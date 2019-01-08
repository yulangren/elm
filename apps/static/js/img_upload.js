window.onload = function () {
    qiniu.setUp({
        'domain': 'http://pksszbfpa.bkt.clouddn.com/',
        'browse_btn': 'upload-btn',
        'uptoken_url': '/uptoken/',
        'success': function (up, file, info) {
            let image_url = file.name;
            let input = document.getElementById('shop_img');
            input.value = image_url;
            let img = document.getElementById('img');
            img.setAttribute('src', image_url + '?imageView2/1/w/50/h/50/q/75|imageslim');
        }
    });
};
