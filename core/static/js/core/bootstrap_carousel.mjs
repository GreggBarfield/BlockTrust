export class BootstrapCarousel {
    constructor(imageURLs, attachTo) {
        let frame = attachTo;
        let box = document.createElement("div");
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

            let img = document.createElement("div");
            img.style.width = "100%";
            img.style.height = "100%";
            img.style.backgroundImage = "url(" + image + ")";
            img.style.backgroundSize = "cover";
            img.style.backgroundPosition = "center";
            img.src = image;
            item.append(img);
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
}