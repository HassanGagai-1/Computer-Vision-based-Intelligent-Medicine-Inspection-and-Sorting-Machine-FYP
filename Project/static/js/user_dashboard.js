function showToastMessage(type, text) {
    switch (type) {
        case 'success':
            toastr.success(text);
            break;
        case 'info':
            toastr.info(text);
            break;
        case 'error':
            toastr.error(text);
            break;
        case 'warning':
            toastr.warning(text);
            break;
        default:
            console.error('Invalid toast type');
            break;
    }
}
function myshowLoader() {
    document.querySelector('.loader-wrapper').style.display = 'flex';
}
    
function myhideLoader() {
    document.querySelector('.loader-wrapper').style.display = 'none';
}