import { InfoModal } from "./info_modal.mjs";

export class BootstrapCarousel {
    constructor(imageURLs, attachTo,type) {
        let frame = attachTo;
        this.frame = frame;
        this.isFullScreen = false;
        this.modal = null;


        let box = document.createElement("div");
        this.box = box;
        box.style.overflow = "hidden";
        box.style.height = "100%";
        box.className = "carousel slide";
        let carouselIndicators = document.createElement("div");
        carouselIndicators.className = "carousel-indicators";
        box.append(carouselIndicators);

        let carouselInner = document.createElement("div");
        carouselInner.className = "carousel-inner";
        carouselInner.style.height = "100%";
        box.append(carouselInner);

        let tabs = [];

        for (const image of imageURLs) {
            let li = document.createElement("li");
            tabs.push(li);
            carouselIndicators.append(li);

            let item = document.createElement("div");
            item.className = "carousel-item";
            item.style.width = "100%";
            item.style.height = "100%";
            carouselInner.append(item);

            if(type=="img"){
                let img = document.createElement("div");
                img.style.width = "100%";
                img.style.height = "100%";
                img.style.backgroundImage = "url(" + image + ")";
                img.style.backgroundSize = "cover";
                img.style.backgroundPosition = "center";
                img.src = image;
                item.append(img);
            }
            else if(type=="video")
            {
                console.log(image)
                let embedblock=document.createElement("div");
                embedblock.className="embed-responsive embed-responsive-16by9";
                item.append(embedblock);
                let link = document.createElement("iframe");
                link.className="embed-responsive-item"
                link.type="text/html";
                link.src=image;
                embedblock.append(link);
            }
            
        }

        if (imageURLs.length > 0) {
            carouselIndicators.children[0].className += " active";
            carouselInner.children[0].className += " active";
        }
            
        function createButton(className, text, fc) {
            let b = document.createElement("div");
            b.className = "carousel-control-" + className;
            let icon = document.createElement("span");
            icon.className = "fas fa-chevron-" + fc;
            b.append(icon);
            let t = document.createElement("span");
            t.className = "sr-only";
            t.textContent = text;
            b.append(t);
            return b;
        }
        let previous = createButton("prev", "Previous", "left");
        box.append(previous);
        let next = createButton("next", "Next", "right");
        box.append(next);

        let carouselFullscreenBox = document.createElement("div");
        this.carouselFullscreenBox = carouselFullscreenBox;
        carouselFullscreenBox.style.position = "absolute";
        carouselFullscreenBox.style.right = "0px";
        carouselFullscreenBox.style.bottom = "0px";
        carouselFullscreenBox.style.width = "15%";
        carouselFullscreenBox.style.height = "23px";
        carouselFullscreenBox.style.display = "flex";
        carouselFullscreenBox.style.justifyContent = "center";
        carouselFullscreenBox.style.alignItems = "center";
        carouselFullscreenBox.style.zIndex = 3;
        carouselFullscreenBox.style.cursor = "pointer";
        carouselFullscreenBox.addEventListener("click", ()=>{this.goFullScreen();});
        box.append(carouselFullscreenBox);

        let carouselFullscreenIcon = document.createElement("i");
        carouselFullscreenIcon.className = "fas fa-expand";
        carouselFullscreenIcon.style.fontSize = "12px";
        carouselFullscreenIcon.style.color = "white";
        carouselFullscreenBox.append(carouselFullscreenIcon);

        frame.append(box);
        $(box).carousel();
        $(previous).click(()=>{$(box).carousel('prev')});
        $(next).click(()=>{$(box).carousel('next')});
        for (let i = 0; i < tabs.length; i++) {
            tabs[i].addEventListener("click", ()=>{
                $(box).carousel(i);
            });
        }
    }

    goFullScreen() {
        if (this.isFullScreen) {
            return;
        }
        this.isFullScreen = true;

        this.modal = new InfoModal("Sales Group Media", null);
        this.box.remove();
        this.modal.getBody().append(this.box);
        this.modal.getBody().style.height = "400px";
        this.modal.getBody().style.position = "relative";
        this.modal.getBody().style.padding = "0px";

        this.carouselFullscreenBox.style.display = "none";

        this.modal.closedPromise.then(()=>{
            this.frame.append(this.box);
            this.modal = null;
            this.isFullScreen = false;
            this.carouselFullscreenBox.style.display = "flex";
        });
    }
}
