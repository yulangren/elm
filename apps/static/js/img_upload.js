window.onload = function () {
    qiniu.setUp({
        'domain': 'http://pksszbfpa.bkt.clouddn.com/',
        'browse_btn': 'upload-btn',
        'uptoken_url': '/uptoken/',
        'success': function (up, file, info) {
            let image_url = file.name;
            let image_input = document.getElementById('shop_img');
            image_input.value = image_url;
        }
    });
};
