$(document).ready(function(){
	baseURL = "http://118.25.122.180:8000";
	if(window.sessionStorage.userId){
		$(".usrId").text("用户"+window.sessionStorage.userId);
		logOut = "<a class=\"logOut\">"
		+"<i class=\"fa fa-sign-out\" ></i> 登出"
		+"</a>";
		dropdownBtn = "<span class=\"text-muted text-xs block\">更多...<b class=\"caret\"></b></span>";
		dropdownMenu = "<li><a id=\"checkHistory\">查看历史评分</a></li>"
		+"<li><a class=\"logOut\">注销</a></li>";
		$(".logBtn").append(logOut);
		
		$(".more").append(dropdownBtn);
		$(".ddMenu").append(dropdownMenu);
		$(".logOut").click(function(){
			window.sessionStorage.removeItem("userId");
			window.location.reload();
		});
		$("#checkHistory").click(function(){
            //usrId = 200;
            $("#historyModal").modal();
            $.ajax({
            	type:'get',
            	url:baseURL+"/getHistoricalData?"+"usrId="+window.sessionStorage.userId,
            	dataType:'jsonp',
            	jsonp:'callback',
            	jsonpCallback:"successCallback",
            	success: function (data) {

            		arr = data;
            		arr1 = new Array();
            		count = 0;
            		for(var i in arr){
            			for(var j in arr[i]){
            				arr1[count] = arr[i][j];
            				count++;
            			}
            		}
            		if(count != 0 ){
            			var pagesize = 10;
            			for(var i=0;i<10;i++)
            			{
            				$('.showlabel').eq(i).text(arr1[i]);
            			} 
            			var pager = window.amPagination('#ampagination-bootstrap',{
            				page:1,
            				totals:count,
            				pageSize:10,
            				theme:'bootstrap',
            				btnSize:'lg'
            			})
            			pager.onChangePage(function(e){
            				for(var i=0;i<10;i++)
            				{
            					if(((e.page-1)*10+i)<count)
            						$('.showlabel').eq(i).text(arr1[(e.page-1)*10+i]);
            					else
            						$('.showlabel').eq(i).text("");
            				}          
            			});
            		}
            	}
            });

            
        });
	}else{

		logIn = "<a data-toggle=\"modal\" data-target=\"#myModal6\" class=\"logIn\">"
		+"<i class=\"fa fa-sign-in\" ></i> 登录"
		+"</a>";
		$(".logBtn").append(logIn);
		$(".logIn").click(function(){
			
			$(".logInBtn").click(function(){
				email = $(".userEmail").val();
				password = $(".userPassword").val();
				$.ajax({
					type:'get',
					url:baseURL+'/login?email='+email+"&psw="+password+"&usr_id=-1",
					dataType:'jsonp',
					jsonp:'callback',
					jsonpCallback:"successCallback",
					success:function(data){
						if(data.status == "logged_email" || data.status == "logged_num"){
							window.sessionStorage.userId = data.usr_id;
							window.location.reload();
						}
						else{
							alert("账号或密码错误");
						}
					}
				}); 
			});


			$(".testBtn").click(function(){
				tempId = $(".userEmail").val();
				$.ajax({
					type:'get',
					url:baseURL+"/login?email=none&usr_id="+tempId,
					dataType:'jsonp',
					jsonp:'callback',
					jsonpCallback:"successCallback",
					success:function(data){
						if(data.status == "logged_email" || data.status == "logged_num"){
							window.sessionStorage.userId = tempId;
							window.location.reload();
						}
						else{
							alert("账号或密码错误");
						}
					}
				}); 
			});

			$(".beginSignUp").click(function(){
				$(".signUpBtn").click(function(){
					email = $(".signUpEmail").val();
					password = $(".signUpPassword1").val();
					$.ajax({
						type:'get',
						url:baseURL+'/register?email='+encodeURIComponent(email)+"&psw="+password,
						dataType:'jsonp',
						jsonp:'callback',
						jsonpCallback:"successCallback",
						success:function(data){
							if(data.status == "registered"){
								window.sessionStorage.userId = data.usrId;
								window.location.reload();
							}else if(data.status == "email_exist"){
								alert("邮箱已存在");
							}else{
								alert("未知错误");
							}
						}
					}); 
				})
			});
		});



		


	}

});