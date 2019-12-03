
function subtractMonth() {
    var month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    var month_display = document.querySelector('.month').textContent;
    var year_display = parseInt(document.querySelector('.year').textContent);
    var index = month_list.indexOf(month_display);
    if (month_display!='January'){
        month_display = month_list[index-1];
        document.querySelector('.month').textContent = month_display;
    }
    else{
        month_display = 'December'
        year_display -= 1
        document.querySelector('.month').textContent = month_display;
        document.querySelector('.year').textContent = year_display;
    }
    return [month_display, year_display]
}

function addMonth() {
    var month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    var month_display = document.querySelector('.month').textContent;
    var year_display = parseInt(document.querySelector('.year').textContent);
    var index = month_list.indexOf(month_display);
    if (month_display!='December'){
        month_display = month_list[index+1];
        document.querySelector('.month').textContent = month_display;
    }
    else{
        month_display = 'January'
        year_display += 1
        document.querySelector('.month').textContent = month_display;
        document.querySelector('.year').textContent = year_display;
    }
    return [month_display, year_display]
}


