var locked;
window.onload = function () {
	slide();
	//禁止F12
	// $("*").keydown(function (e) {//判断按键
	// 	e = window.event || e || e.which;
	// 	if (e.keyCode == 123) {
	// 		e.keyCode = 0;
	// 		return false;
	// 	}
	// });
	//禁止审查元素
	// $(document).bind("contextmenu",function(e){
	// 	return false;
	// });
}
window.onresize = function () {
	if(locked==true){
		var boxWidth = $('#slide_box').width();
		$('#slide_xbox').width(boxWidth);
	}else{
		slide();
	}
}
	  //滑动解锁移动
function slide() {
	var slideBox = $('#slide_box')[0];
	var slideXbox = $('#slide_xbox')[0];
	var btn = $('#btn')[0];
	var slideBoxWidth = slideBox.offsetWidth;
	var btnWidth = btn.offsetWidth;
	//pc端
	btn.ondragstart = function () {
		return false;
		
		
	};
	btn.onselectstart = function () {
		return false;
	};
	btn.onmousedown = function (e) {
		var disX = e.clientX - btn.offsetLeft;
		document.onmousemove = function (e) {
			var objX = e.clientX - disX + btnWidth;
			if (objX < btnWidth) {
				objX = btnWidth
			}
			if (objX > slideBoxWidth) {
				objX = slideBoxWidth
			}
			$('#slide_xbox').width(objX + 'px');
		};
		document.onmouseup = function (e) {
			var objX = e.clientX - disX + btnWidth;
			if (objX < slideBoxWidth) {
				objX = btnWidth;
			} else {
				objX = slideBoxWidth;
				locked = true;
				$('#slide_xbox').html('验证通过<div id="btn"><i class="iconfont icon-xuanzhong" style="color: #35b34a;"></i></div>');
				$('#btn').css('background-image','url(images/duihao.png)')
			}
			$('#slide_xbox').width(objX + 'px');
			document.onmousemove = null;
			document.onmouseup = null;
		};
	};
	
	
	//移动端
	var cont = $("#btn");
	var startX = 0, sX = 0, moveX = 0,leftX = 0;
	cont.on({//绑定事件
		touchstart: function (e) {
			startX = e.originalEvent.targetTouches[0].pageX;//获取点击点的X坐标
			sX = $(this).offset().left;//相对于当前窗口X轴的偏移量
			leftX = startX - sX;//鼠标所能移动的最左端是当前鼠标距div左边距的位置
		},
		touchmove: function (e) {
			e.preventDefault();
			moveX = e.originalEvent.targetTouches[0].pageX;//移动过程中X轴的坐标
			var objX = moveX - leftX + btnWidth;
			if (objX < btnWidth) {
				objX = btnWidth
			}
			if (objX > slideBoxWidth) {
				objX = slideBoxWidth
			}
			$('#slide_xbox').width(objX + 'px');
		},
		touchend: function (e) {
			var objX = moveX - leftX + btnWidth;
			if (objX < slideBoxWidth) {
				objX = btnWidth;
			} else {
				objX = slideBoxWidth;
				locked = true;
				$('#slide_xbox').html('验证通过<div id="btn"><i class="iconfont icon-xuanzhong" style="color: #35b34a;"></i></div>');
				$('#btn').css('background-image','url(images/duihao.png)')
			}
			$('#slide_xbox').width(objX + 'px');
		}
	});
}