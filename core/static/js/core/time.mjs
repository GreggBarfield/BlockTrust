export function formatDate(epoch) {
    if (epoch == null || epoch <= 0)
        return "--";
    let d = new Date(epoch * 1000);
    return (d.getMonth() + 1) + "/" + d.getDate() + "/" + d.getFullYear();
}
