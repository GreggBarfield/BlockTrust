function makeDouble(value) {
    if (value < 10) {
        return "0" + value;
    }
    return "" + value;
}

export function formatDate(epoch) {
    if (epoch == null || epoch <= 0)
        return "--";
    let d = new Date(epoch * 1000);
    return (d.getMonth() + 1) + "/" + makeDouble(d.getDate()) + "/" + d.getFullYear();
}

export function formatDateTime(epoch) {
    if (epoch == null || epoch <= 0)
        return "--";
    let d = new Date(epoch * 1000);
    return (d.getMonth() + 1) + "/" + makeDouble(d.getDate()) + "/" + d.getFullYear()
        + " " + d.getHours() + ":" + makeDouble(d.getMinutes());
}
