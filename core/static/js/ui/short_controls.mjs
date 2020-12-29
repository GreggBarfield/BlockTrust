/** Simple short controls. */
export class ShortControls {
    /**
     * Constructs ShortControls.
     * 
     * @param {Node} attachTo The Node to intially attach UI
     */
    constructor(attachTo) {
        this.frame = attachTo;
    }

    /**
     * Adds a button.
     * 
     * @param {string} text The text of the button (displayed)
     * @param {string} className The class(es) to apply
     * @param {function} [click] On-click callback
     * 
     * @returns {Node} The DOM node created
     */
    addButton(text, className, click=null) {
        let button = document.createElement("button");
        button.textContent = text;
        button.className = className;
        button.type = "button";
        this.frame.appendChild(button);
        if (click !== null) {
            button.addEventListener("click", click);
        }
        return button;
    }

    /**
     * Adds an 'a' tag.
     * 
     * @param {string} text The text of the link (displayed)
     * @param {string} className The class(es) to apply
     * @param {function} href Link to open
     * 
     * @returns {Node} The DOM node created
     */
    addA(text, className, href) {
        let a = document.createElement("a");
        a.textContent = text;
        a.className = className;
        a.href = href;
        this.frame.appendChild(a);
        return a;
    }
}
