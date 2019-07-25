$(document).ready(function(){

	baseURL = "http://118.25.122.180:8000";
	//baseURL = "http://10.72.51.183:8001";
	arr = new Array();
	currentUserId = "*";
	function bindDetailedMovieInfo(data){
		memberName = "movie"+data.id;
	}
	function createMoviePanel(data,no,type){
		if((data.title).charAt(0) == '[')
			movieName = (data.title).slice(2,-2);
		else
			movieName = data.title;
		if(window.sessionStorage.userId)
			movieReason = type?"评分喜好推荐":"最近浏览推荐";
		else
			movieReason = "";
		movieIntro = (data.intro).length>100?(data.intro).substring(0,100)+"...":data.intro;
		movieDir = data.dir;
		moviePic = data.pic;
		movieId = data.id;
		memberName = "movie"+data.id;
		if(movieIntro == "" || movieIntro == "[]"){
			movieIntro = "暂无简介...";
		}
		if(movieDir == ""){
			movieDir = "暂无导演信息";
		}
		if(moviePic == ""){
			moviePic = "<img src=\"img/movie_default_large.png\" class=\"carousel-inner img-responsive\">"
			//"<div class=\"product-imitation\">"
			//+"[ 暂无图片 ]"
			//+"</div>"
		}else{
			moviePic = "<img src="+moviePic+" class=\"carousel-inner img-responsive\">";
		}
		html = "<div class=\"col-md-2\">"
		+"<div class=\"ibox\">"
		+"<div class=\"ibox-content product-box\">"
		+moviePic                                                              
		+"<div class=\"product-desc\">"
		+"<a class=\"product-name\">"+movieName+"</a>"
		+"<small class=\"text-muted\"> "+movieDir+"</small>"
		                                    
		+"<div class=\"small m-t-xs\">"
		+movieIntro
		+"</div>"
		+"<div class=\"m-t text-righ\">"
		+"<a id="+memberName+" href=\"single_movie_detail.html?id="+movieId+"\" class=\"btn btn-xs btn-outline btn-primary\"> 电影详情 <i class=\"fa fa-long-arrow-right\"></i> </a>"
		+"</div>"
		+"<div class=\"small\"> "+movieReason+"</div>"  
		+"</div>"
		+"</div>"
		+"</div>"
		+"</div>";
		if(no<=5)
			$("#scanMovieContainer1").append(html);
		else if(no<=9)
			$("#scanMovieContainer2").append(html);
		// else
		// 	$("#scanMovieContainer3").append(html);

		var recordurl = "http://10.72.51.183:8001";
		if(window.sessionStorage.userId){
			$("a#"+memberName).click(function(){
				$.get(recordurl+"/records/?movie="+data.id+"&usr="+window.sessionStorage.userId, function(result){
	    			console.log(result);
	  			});
			});
		}
	}

	if(window.sessionStorage.userId){
		currentUserId = window.sessionStorage.userId;
		
	}

	

	$.ajax({
		type:'get',
		url:baseURL+"/getUsrRecMsg/?usrId="+currentUserId,
		dataType:'jsonp',
		jsonp:'callback',
		jsonpCallback:"successCallback",

		success:function(data){
			arr = data.recMovie;
			records = data.records;
			console.log(typeof(data.records));
			no = 0;
			html = "";
			jsonData = JSON.parse(arr);
			for(var i in jsonData){             
				console.log($.inArray(jsonData[i].id, records));
				createMoviePanel(jsonData[i],i,$.inArray(jsonData[i].id, records)==-1);
			}             
            }/*,
            error:function(XMLHttpRequest, textStatus, errorThrown){
                 alert(XMLHttpRequest.status);
                 alert(XMLHttpRequest.readyState);
                 alert(textStatus);
             }*/
         }); 
	
});