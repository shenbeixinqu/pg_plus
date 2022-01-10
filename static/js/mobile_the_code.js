//获取手机验证码
	var InterValObj; //timer变量，控制时间
	var count = 60; //间隔函数，1秒执行
	var curCount;//当前剩余秒数

	function sendMessage() {
	  　curCount = count;
	　　//设置button效果，开始计时
		 $("#btnSendCode").attr("disabled", "true");
		 $("#btnSendCode").val("" + curCount + "秒后重新获取");
		 InterValObj = window.setInterval(SetRemainTime, 1000); //启动计时器，1秒执行一次
		 var dealType ="";
		 var uid = "";
		 var code = "";
	　　  //向后台发送处理数据
		 $.ajax({
		 　　type: "POST", //用POST方式传输
		 　　dataType: "JSON", //数据格式:JSON
		 　　url: '', //目标地址
		　　 data: "dealType=" + dealType +"&uid=" + uid + "&code=" + code,
		　　 error: function (data) { },
		 　　success: function (msg){ }
		 });
	}
	
	//timer处理函数
	function SetRemainTime() {
		if (curCount == 0) {                
			window.clearInterval(InterValObj);//停止计时器
			$("#btnSendCode").removeAttr("disabled");//启用按钮
			$("#btnSendCode").val("重新获取验证码").css({"background-color":"#0097a8"});
		}
		else {
			curCount--;
			$("#btnSendCode").val("" + curCount + "秒后重新获取").css({"background-color":"#D1D4D3"});
		}
	}
			
			
//*********获取语音验证码*********//

	var AddInterValObj; //timer变量，控制时间
	var adcount = 60; //间隔函数，1秒执行
	var addCount;//当前剩余秒数
	
	function sendAddmes() {
		var myreg = /^(((13[0-9]{1})|(15[0-9]{1})|(18[0-9]{1}))+\d{8})$/; 
		if(!myreg.test($("#add_phone").val())) 
		{ 
			layertest('请输入有效的手机号码')
		    return false;
		}else{
			addCount = adcount;
		　　//设置button效果，开始计时
			 $("#addSendCode").attr("disabled", "true");
			 $("#addSendCode").val("" + addCount + "秒后重新获取").css({"background-color":"#D1D4D3"});
			 AddInterValObj = window.setInterval(SetAddnTime, 1000); //启动计时器，1秒执行一次
			 var dealType ="";
			 var uid = "";
			 var code = "";
			 var $phone = $("#add_phone").val()
		　　  //向后台发送处理数据
			 $.ajax({
			 　　type: "GET", //用POST方式传输
			 　　contentType: 'application/json', //数据格式:JSON
			 　　url: '{{ url_for("api.message") }}', //目标地址
			// 　　 data: "dealType=" + dealType +"&uid=" + uid + "&code=" + code,
			　　 data: {phone: $phone,sort: 6},
				 error: function (data) { },
			 　　success: function (msg){ }
			 });
		}
	}
	
	//timer处理函数
	function SetAddnTime() {
		if (addCount == 0) {                
			window.clearInterval(AddInterValObj);//停止计时器
			$("#addSendCode").removeAttr("disabled");//启用按钮
			$("#addSendCode").val("重新获取验证码").css({"background-color":"#0097a8"});
		}
		else {
			addCount--;
			$("#addSendCode").val("" + addCount + "秒后重新获取").css({"background-color":"#D1D4D3"});
		}
	}
	
	function telphone(){
		var myreg = /^(((13[0-9]{1})|(15[0-9]{1})|(18[0-9]{1}))+\d{8})$/; 
		if(!myreg.test($("#add_phone").val())) 
		{ 
			layertest('请输入有效的手机号码');
			$('.login_ipt').addClass('error');
		    return false;
		}else{
			$('.login_ipt').removeClass('error');
		}
	}
	$(document).on('blur','.login_ipt',function(){
		telphone();
	});
	
	//code 验证
	function code_test(){
		if($('#code').val()==''){
			layertest('验证码不能为空');
			$('#code').addClass('error');
		}else{
			$('#code').removeClass('error');
		}
	}
	$(document).on('blur','.code',function(){
		code_test();
	});
	
	// layer modal
	function layertest(content){
		layer.open({
		    content: content
		    ,btn: '我知道了'
		});
	}
	//layer loading
	function loading(content){
		layer.open({
		    type: 2
		    ,content: content
		});
	}
	
	// update btn click
	$(document).on('click','.updateBtn',function(){
		if($('.error').length >0){
			layertest('请您填写正确的资料')
		}else{
			loading('跳转中')
		}
	})
