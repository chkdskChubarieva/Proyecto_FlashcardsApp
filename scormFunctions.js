
var API = null;

function findAPI(win) {
    while ((win.API == null) && (win.parent != null) && (win.parent != win)) {
        win = win.parent;
    }
    return win.API;
}

function scormInitialize() {
    API = findAPI(window);
    if (API == null) {
        console.log("No se pudo encontrar el API SCORM");
        return false;
    }
    return API.LMSInitialize("");
}

function scormTerminate() {
    if (API == null) return;
    return API.LMSFinish("");
}

function scormGet(parameter) {
    if (API == null) return "";
    return API.LMSGetValue(parameter);
}

function scormSet(parameter, value) {
    if (API == null) return "false";
    return API.LMSSetValue(parameter, value);
}

function scormCommit() {
    if (API == null) return "false";
    return API.LMSCommit("");
}
