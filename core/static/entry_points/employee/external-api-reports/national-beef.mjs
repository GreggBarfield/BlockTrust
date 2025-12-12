document.addEventListener('DOMContentLoaded', async() => {
    const response = await fetch(`/employee/fetch-api-inserts-report-by-account`, {
            method: 'POST',
            body: JSON.stringify({account_id: national_beef_account_id}),
            headers: {"Content-type": "application/json; charset=UTF-8"}
    });
    const data = await response.json();
    let reportTableColumns = [{"data": 'inserts_date', "title": "Date", "type": 'date'}, {"data": 'inserts_count', "title": "Number of Inserts"}, {"data": "processed_inserts_count", "title": "Number of Inserts Processed Successfully"}, {"data": 'total_animals_updated_count', "title": "Total Animal Records Updated"}]
    if("daily_api_inserts_counts" in data){
        let dailyApiInsertsCounts = data.daily_api_inserts_counts;
        $('#api-report-table').DataTable({columns: reportTableColumns, pageLength:50});
        $('#api-report-table').DataTable().rows.add(dailyApiInsertsCounts).draw();
    }
});