function addNewRow(thisRow) {
    if (document.createElement && document.childNodes) {
        let parentRow = document.getElementById("schCrit");
        const schCount = 5;
        if (parentRow.children.length == schCount) {
            alert("Only a maximum of " + schCount + " schedules can be added");
        } else {
            let uniqueId = Math.floor(1000 + Math.random() * 9000);
            let newElement = thisRow.cloneNode(true);
            newElement.id = "critDiv_" + uniqueId;
            thisRow.parentNode.insertBefore(newElement, thisRow.nextSibling);
            updateHelpDeskElementName(newElement, uniqueId);
            document.getElementById("days_" + uniqueId).value = "";
            document.getElementById("hours_" + uniqueId).value = "";
            document.getElementById("mins_" + uniqueId).value = -1;
        }
    }
}

function updateHelpDeskElementName(rowObj, newId) {
    for (let i = 0; i < rowObj.childNodes.length; i++) {
        let tags = rowObj.childNodes[i];
        if (tags.name != undefined && tags.name.indexOf("days") >= 0) {
            tags.name = "days_" + newId;//No I18N
            tags.id = "days_" + newId;//No I18N
        } else if (tags.name != undefined && tags.name.indexOf("hours") >= 0) {
            tags.name = "hours_" + newId;//No I18N
            tags.id = "hours_" + newId;//No I18N
        } else if (tags.name != undefined && tags.name.indexOf("mins") >= 0) {
            tags.name = "mins_" + newId;//No I18N
            tags.id = "mins_" + newId;//No I18N
        }
    }
}

function removeRow(theRow) {
    if (document.createElement && document.childNodes) {
        let thisRow = document.getElementById("schCrit");
        if (thisRow.children.length == 1) {
            alert("Minimum of one condition is needed");
        } else {
            deleteScheduleRow(theRow.parentNode);
        }
    }
}

function deleteScheduleRow(rowObj) {
    rowObj.parentNode.removeChild(rowObj);
}

function validateData() //TODO
{
    let schTempName = document.getElementById("schTempName").value;
    if (schTempName == "") {
        alert("Provide a valid schedule name!")
        return;
    } else {
        //do api call check for name already exists
    }
    let resultJson = {};
    resultJson['schName'] = schTempName;
    let rowListObj = document.getElementById('schCrit');
    let rowlistLen = rowListObj.children.length;
    let timeArray = [];
    for (let i = 0; i < rowlistLen; i++) {
        let rowName = rowListObj.childNodes[i].nextSibling;
        let htmlStr = rowName.innerHTML;
        let rId = htmlStr.split("_")[1].substring(0, 4);
        let days = document.getElementById('days_' + rId).value;
        let hours = document.getElementById('hours_' + rId).value;
        let mins = document.getElementById('mins_' + rId).value;
        if (days == "" || hours == "" || mins == -1) {
            alert("Pls give proper values"); //NO I18N
            return;
        } else {
            let ansJson = {};
            if (parseInt(days) > 99 || parseInt(days) < 0) {
                alert("Please provide days greater than 0 and less than 100");
                return;
            }
            if (parseInt(hours) > 23 || parseInt(hours) < 0) {
                alert("Please provide valid time in 24 hrs format");
                return;
            }
            ansJson["days"] = days;
            ansJson["hours"] = hours;
            ansJson["mins"] = mins;
            timeArray.push(ansJson);
        }
    }
    resultJson['timings'] = timeArray;
    alert(JSON.stringify(resultJson));
}

function validateAddToCart() {
    let cxName = document.getElementById("cxName").value;
    let cxItems = document.getElementById("cxItems").value;
    if (cxName == "" || cxItems == "") {
        alert("Please provide valid details")
        return;
    }
    let httpRequest = new XMLHttpRequest();
    httpRequest.open("POST", "http://localhost:9090/addOrder");
    httpRequest.setRequestHeader('Content-Type', 'application/json');
    let detailsJson = {};
    detailsJson['name'] = cxName;
    detailsJson['count'] = cxItems;
    params = JSON.stringify(detailsJson);
    httpRequest.send(params);
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            let responseJson = JSON.parse(httpRequest.responseText).status;
            console.log(responseJson);
        }
    }
}

function setDefaultTemplate(rowData) {
    alert(rowData.parentNode.parentNode.querySelector("span").value);
}