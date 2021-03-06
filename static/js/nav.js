//字体设置
(function(doc, win) {
	

	
  
    var docEl = doc.documentElement,
        isIOS = navigator.userAgent.match(/iphone|ipod|ipad/gi),
        dpr = isIOS ? Math.min(win.devicePixelRatio, 3) : 1,
        dpr = window.top === window.self ? dpr : 1, //被iframe引用时，禁止缩放
        dpr = 1, // 首页引用IFRAME，强制为1
        scale = 1 / dpr,
        resizeEvt = 'orientationchange' in window ? 'orientationchange' : 'resize';
    docEl.dataset.dpr = win.devicePixelRatio;
    if (navigator.userAgent.match(/iphone/gi) && screen.width == 375 && win.devicePixelRatio == 2) {
        docEl.classList.add('iphone6')
    }
    if (navigator.userAgent.match(/iphone/gi) && screen.width == 414 && win.devicePixelRatio == 3) {
        docEl.classList.add('iphone6p')
    }
    var metaEl = doc.createElement('meta');
    metaEl.name = 'viewport';
    metaEl.content = 'initial-scale=' + scale + ',maximum-scale=' + scale + ', minimum-scale=' + scale;
    docEl.firstElementChild.appendChild(metaEl);
    var recalc = function() {
        var width = docEl.clientWidth;
        if (width / dpr > 640) {
            width = 640 * dpr;
        }
        docEl.style.fontSize = 100 * (width / 640) + 'px';
    };
    recalc();
    // 随着窗口变化而改变
    $(window).resize(function(event) {
		recalc();
	});
    if (!doc.addEventListener) return;
    // win.addEventListener(resizeEvt, recalc, false);
	
	
	
	
	

	
})(document, window);



