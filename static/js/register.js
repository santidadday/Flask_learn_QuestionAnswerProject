// 整个网页加载完成之后再执行
function bindEmailCaptchaClick() {
    $('#captcha-btn').click(function (event) {
        var $this = $(this);
        // 阻止默认事件
        event.preventDefault();
        var email = $('#exampleInputEmail1').val();
        $.ajax({
            url: '/auth/captcha/email?email=' + email,
            method: 'GET',
            success: function (result) {
                var code = result['code'];
                if (code == 200) {
                    var countdown = 60;
                    // 倒计时开始时取消点击事件
                    $this.off('click')
                    var timer = setInterval(function () {
                        $this.text(countdown);
                        countdown -= 1;
                        if (countdown <= 0) {
                            // 清理定时器
                            clearInterval(timer);
                            $this.text('获取验证码')
                            // 倒计时结束后恢复点击事件
                            bindEmailCaptchaClick();
                        }
                    }, 1000)
                    // alert('邮箱验证码发送成功！');
                } else {
                    alert(result['message']);
                }
            },
            fail: function (error) {
                console.log(error)
            }
        })
    });
}

$(function () {
    bindEmailCaptchaClick();
});