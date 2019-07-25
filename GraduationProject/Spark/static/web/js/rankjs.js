$(document).ready(function(){
	baseURL = "http://118.25.122.180:8000";
	//baseURL = "http://10.72.51.183:8001";
	function createRankList(num,data){
		if((data.title).charAt(0) == '[')
			movieName = (data.title).slice(2,-2);
		else
			movieName = data.title;
		movieIntro = (data.intro).length>100?(data.intro).substring(0,100)+"...":data.intro;
		movieDir = data.dir;
		moviePic = data.pic;
		movieId = data.id;
		if(movieIntro == "" || movieIntro == "[]"){
			movieIntro = "暂无简介...";
		}
		if(movieDir == ""){
			movieDir = "暂无导演信息";
		}
		if(moviePic == ""){
			moviePic = "img/movie_default_large.png";
		}else{
			moviePic = moviePic;
		}
		console.log(moviePic);
		if(num==0){
		html = '<div class="row">'
		+'<div class="col-lg-12">'
		+'<div class="widget-head-color-box red-bg p-lg text-center">'
		+'<div class="m-b-md">'
		+'<h2 class="font-bold no-margins">'
		+'<i class="fa fa-trophy fa-5x"></i>'
		+'</h2>'
		+'</div>'
		+'<img src="'+moviePic+'" class="center-block m-b-md img-responsive" alt="profile">'
		+'<div>'
		+'<span><h2 class="font-bold"><a style="color:white" href="single_movie_detail.html?id='+movieId+'">'+movieName+'</a></h2></span>'
		+'</div>'
		+'</div>'
		+'<div class="widget-text-box">'
		+'<h4 class="media-heading">'+movieDir+'</h4>'
		+'<p>'+movieIntro+'</p>'
		+'</div>'
		+'</div>'  
		+'</div>';
	}else{
		console.log(num);
		switch(num){
			case '1':
				color = 'yellow-bg';
				picWidth = '200';
				break;
			case '2':
				color = 'navy-bg';
				picWidth = '160';
				break;
			default:
				color = 'lazur-bg';
				picWidth = '120';
				break;
		}
		html = '<div class="row">'
		+'<div class="col-lg-12">'
		+'<div class="widget '+color+' no-padding">'
		+'<div class="p-m">'
		+'<table class="table shoping-cart-table">'
		+'<tbody>'
		+'<tr>'
		+'<td class="desc">'
		+'<h1 class="m-xs font-bold">'+(parseInt(num)+1+"")+'.</h1>'
		+'<dl class="small m-b-none">'
		+'<dt><h2 class="m-xs font-bold"><a style="color:white" href="single_movie_detail.html?id='+movieId+'">'+movieName+'</a></h2></dt>'
		+'</dl>'
		+'<h3 class="m-xs">'+movieDir+'</h3>'
		+'<div class="m-t-sm">'
		+'<p class="m-xs small">'+movieIntro+'</p>'
		+'</div>'
		+'</td>'
		+'<td width="'+picWidth+'">'
		+'<img src="'+moviePic+'" class="carousel-inner img-responsive">'
		+'</td>'
		+'<td></td>'
		+'</tr>'
		+'</tbody>'
		+'</table>'
		+'</div>'
		+'</div>'
		+'</div>'
		+'</div>';
	}
		$('#ranklist').append(html);
	}
	$.ajax({
		type:'get',
		url:baseURL+"/rank/",
		dataType:'jsonp',
		jsonp:'callback',
		jsonpCallback:"successCallback",
		success:function(data){
			rankList = JSON.parse(data.rank);
			for(var i in rankList){
				createRankList(i,rankList[i]);
			}
        }/*,
            error:function(XMLHttpRequest, textStatus, errorThrown){
                 alert(XMLHttpRequest.status);
                 alert(XMLHttpRequest.readyState);
                 alert(textStatus);
             }*/
         }); 
})