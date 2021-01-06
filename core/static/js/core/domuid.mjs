/**
 * Generates a unique ID for a DOM element.
 * @returns {string} The unique ID
 */
export function newDOMUID() {
    return "domuid" + window.DOMUIDNext++;
}
