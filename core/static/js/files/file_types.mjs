const imageTypes = ["png", "jpeg", "jpg", "gif", "bmp"];

function fileTypeIn(fileName, types) {
    let parts = fileName.split(".");
    if (parts.length == 0) {
        return false;
    }
    return types.indexOf(parts[parts.length - 1]) != -1;
}

export function fileNameIsImage(fileName) {
    return fileTypeIn(fileName, imageTypes);
}
