$(function(){
    let divOverlay = $("#overlay");
    let divPresent = $("#present");
    let divQueue = $("#present");
    let divTextStatus = $("#text_status");
    let divStatus = $("#status");
    let presentationQueue = [];
    let presentedQueue = [];
    let finishedThisSession = 0;
    let totalUnapproved = 0;
    let gettingImages = false;
    let currentImage = null;
    
    let divLog = $("#log");

    let waitStatus = $("#wait_status");
    let waitInner = $("#wait_inner");
    let waitOuter = $("#wait_outer");
    let waiting = null;

    let rejectKeys = $("#reject_keys");
    let approveKeys = $("#approve_keys");
    let rejectKeysList = ['a', 's', 'd', 'f'];
    let approveKeysList = ['j', 'k', 'l', ';'];
    let rejectKeysHit = [];
    let approveKeysHit = [];

    function paintKeysHit() {
        let rejectHTML = "";
        let approveHTML = "";
        for (key of rejectKeysList) {
            let c = "not_hit";
            if (rejectKeysHit.includes(key)) {
                c = "hit";
            }
            rejectHTML += "<span class='" + c + "'>" + key + "</span>";
        }
        for (key of approveKeysList) {
            let c = "not_hit";
            if (approveKeysHit.includes(key)) {
                c = "hit";
            }
            approveHTML += "<span class='" + c + "'>" + key + "</span>";
        }
        rejectKeys.html(rejectHTML);
        approveKeys.html(approveHTML);
    }

    function allReady() {
        if (waiting)
            return false;
        if (!currentImage)
            return false;
        if (!currentImage._loaded)
            return false;
        if (divOverlay.css('display') !== 'none')
            return false;
        return true;
    }

    document.onkeydown = function(e) {
        if (!allReady()) {
            startWait();
            return;
        }

        if (rejectKeysList.includes(e.key)) {
            if (approveKeysHit.length != 0 || rejectKeysHit.includes(e.key)) {
                startWait();
            }
            else {
                rejectKeysHit.push(e.key);
            }
        }
        if (approveKeysList.includes(e.key)) {
            if (rejectKeysHit.length != 0 || approveKeysHit.includes(e.key)) {
                startWait();
            }
            else {
                approveKeysHit.push(e.key);
            }
        }

        if (rejectKeysHit.length >= 2) {
            decision('r');
        }
        if (approveKeysHit.length >= 2) {
            decision('a');
        }

        paintKeysHit();
    }

    function hideOverlay() {
        divOverlay.hide();
    }

    function decision(d) {
        if (!allReady()) {
            startWait();
            return;
        }
        let id = currentImage.id
        divLog.prepend(currentImage.id + ": " + d + "<br>");
        if (d=='a')
            setStatusOnImage(currentImage, "status_accepted");
        else if (d=='r')
            setStatusOnImage(currentImage, "status_rejected");
        // Start ajax post
        $.ajax({url:"/approval/decision?id=" + currentImage.id + "&d=" + d})
        .done(function(){
            divLog.prepend(id + ": " + d + " COMPLETED<br>");
        })
        .fail(function(xhr, status, err){
            showOverlay("error during image decision: " + status + " " + err + "<br>" + 
                "The specific error returned was: " + xhr.responseText);
        });

        let m = presentationQueue.shift();
        presentedQueue.push(m);
        divQueue[0].removeChild(currentImage._img);
        delete currentImage._img;
        currentImage = null;
        totalUnapproved -= 1;
        updatePresentation();
    }

    function startWait() {
        if (waiting) {
            clearTimeout(waiting);
        }

        let waitTime = 250;

        rejectKeysHit = [];
        approveKeysHit = [];
        paintKeysHit();

        waitStatus.html("WAIT " + waitTime + "MS");
        waitInner.css({"width": "0%"});
        waitInner.stop();
        waitInner.animate({"width": "100%"}, 250);
        waitInner.removeClass("wait_inner_finished");

        waiting = setTimeout(function() {
            waitStatus.html("REJECT or APPROVE");
            waitInner.addClass("wait_inner_finished");
            waiting = null;
        }, waitTime);
    }

    function showOverlay(h) {
        divOverlay.show();
        divOverlay.html(h);
    }

    function updatePresentation() {
        if (currentImage === null) {
            if (presentationQueue.length === 0) {
                divQueue.html("Searching for images...");
                getImages();
            }
            else {
                currentImage = presentationQueue[0];
            }
        }

        if (presentationQueue.length < 5)
            getImages();

        divTextStatus.html(
              "Remaining unapproved images: " + totalUnapproved + "<br>"
            + "Unapproved images in local queue: " + presentationQueue.length + "<br>"
            + "Decisions made in local queue: " + presentedQueue.length + "<br>");

        if (currentImage) {
            if (currentImage._loaded === false) {
                divQueue.html("Loading image...");
            }
            else {
                if (!(divQueue[0] === currentImage._img.parentNode)) {
                    startWait();
                    hideOverlay();
                    divQueue.html("");
                    divQueue[0].appendChild(currentImage._img);
                    setStatusOnImage(currentImage, "status_present");
                }
            }
        }
    }

    function setStatusOnImage(image, status) {
        image._statusjq.removeClass("status_loading");
        image._statusjq.removeClass("status_loaded");
        image._statusjq.removeClass("status_present");
        image._statusjq.removeClass("status_accepted");
        image._statusjq.removeClass("status_rejected");
        image._statusjq.addClass(status);
    }

    function imageLoaded() {
        for (image of presentationQueue) {
            if (image._img === this) {
                image._loaded = true;
                setStatusOnImage(image, "status_loaded");
                if (currentImage === image) {
                    updatePresentation();
                }
                else if (currentImage === null) {
                    updatePresentation();
                }
            }
        }
    }

    function addImage(data) {
        for (image of presentationQueue) {
            if (image.id === data.id) {
                return;
            }
        }
        for (image of presentedQueue) {
            if (image.id === data.id) {
                return;
            }
        }
        data._img = document.createElement("img");
        data._status = document.createElement("span");
        divStatus[0].appendChild(data._status);
        data._statusjq = $(data._status);
        data._statusjq.addClass("status_box");
        data._status.innerHTML = data.id;
        setStatusOnImage(data, "status_loading");
        data._img.height = 500;
        data._loaded = false;
        data._img.onload = imageLoaded;
        data._img.src = "/static/images/" + data.new_password + "." + data.new_type;

        presentationQueue.push(data);
    }

    function getImages() {
        if (gettingImages)
            return;
        gettingImages = true;
        $.ajax({
            url: '/approval/list'
        })
        .done(function(data){
            totalUnapproved = data.remaining_images;
            if (totalUnapproved == 0) {
                showOverlay("No unapproved images remaining");
            }
            for (image in data.images) {
                addImage(data.images[image]);
            }
            updatePresentation();
        })
        .fail(function(xhr, status, err){
            showOverlay("error during image get: " + status + " " + err + "<br>" + 
                "The specific error returned was: " + xhr.responseText);
        })
        .always(function(){
            gettingImages = false;
        });
    }

    paintKeysHit();
    getImages();
});