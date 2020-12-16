/*
    Prefer not highlighting over highlighting by default to not annoy users.
*/
export function urlHighlighter(sourceText, targetNode) {
    let results = [...sourceText.matchAll(/(https?:\/\/)?[a-zA-Z0-9-_\.]*\.(com|net|org)(\/(\S)*)?/g)];

    // This might already be guaranteed, but just in case...
    results.sort((a, b)=>{
        return a.index - b.index;
    });

    let remainingCharIndex = 0;

    for (const result of results) {
        if (remainingCharIndex != result.index) {
            targetNode.append(document.createTextNode(sourceText.substring(remainingCharIndex, result.index)));
        }

        let a = document.createElement("a");
        let url = result[0];
        if (url.substring(0,4) != "http") {
            url = "https://" + url;
        }
        a.href = url;
        a.textContent = result[0];
        a.target = "_blank";
        targetNode.append(a);

        remainingCharIndex = result.index + result[0].length;
    }

    if (remainingCharIndex != sourceText.length) {
        targetNode.append(document.createTextNode(sourceText.substring(remainingCharIndex)));
    }
}
