$(document).ready(function(){
    baseURL = "http://118.25.122.180:8000";
    //baseURL = "http://10.72.51.183:8001";
    function GetRequest() {
        var url = location.search; 
        if (url.indexOf("?") != -1)
            var str = url.substr(1);
        strs = str.split("=");
        return strs[1];
    }

    


    function createAmovie(movieName,moviePic,movieIntro,movieDir,movieID,movieType){

        movieIntr = movieIntro.length>100?movieIntro.substring(0,100)+"...":movieIntro;
        if(movieIntro == "[]"){
            movieIntr = "暂无简介...";   
        }
        movieTp = (movieType.slice(1,-1)).replace(/ /g,"");
        if((movieName).charAt(0) == '[')
            movieName = (movieName).slice(2,-2);
        else
            movieName = movieName;
        tempType = movieTp.split(',')
        formatMovieType = "";
        for(var i in tempType){
            formatMovieType += tempType[i].slice(1,-1);
            formatMovieType += '/';
        }
        formatMovieType = formatMovieType.slice(0,-1);
        if(moviePic == "" || moviePic == "#" || moviePic == "[]")
            moviePic = "img/movie_default_large.png";
        html = "<div class=\"ibox-content\">"
        +"<div class=\"table-responsive\">"
        +"<table class=\"table shoping-cart-table\">"
        +"<tbody>"
        +"<tr>"
        +"<td width=\"180\">"
        +"<img src="+ moviePic+" class=\"carousel-inner img-responsive\">"
        +"</td>"
        +"<td class=\"desc\">"
        +"<h3>"
        +"<a href=\"single_movie_detail.html?id="+movieID+"\" class=\"text-navy\">"
        +movieName
        +"</a>"
        +"</h3>"
        +"<dl class=\"small m-b-none\">"
        +"<dt>"+movieDir+"</dt>"
        +"</dl>"
        +"<p class=\"small\">"
        +movieIntr
        +"</p>"
        +"<div class=\"m-t-sm\">"
        +"<p class=\"small\">"+formatMovieType+"</p>"
        +"</div>"
        +"</td>"
        +"<td>"
        //+"<h4>4.0</h4>"
        +"</td>"
        +"</tr>"
        +"</tbody>"
        +"</table>"
        +"</div>"
        +"</div>";
        $(".movieContainer").append(html);
    };
    movieName = "";
    $('#rating-input').rating({
        min: 0,
        max: 5,
        step: 1,
        size: 'lg',
        showClear: false,
        showCaption: false

    });
    hasRate = false;
    $('#rating-input').on('rating.change', function () {
        if(window.sessionStorage.userId  && !hasRate){
            currentUserId = window.sessionStorage.userId;
            $.ajax({
                type:'get',
                url:baseURL+"/rateTheMovie/?usrId="+currentUserId+"&movieTitle="+movieName+"&ratings="+$('#rating-input').val(),
                dataType:'jsonp',
                jsonp:'callback',
                jsonpCallback:"successCallback",

                success:function(data){
                    if(data.status == "success_rate_the_movie"){
                        swal({
                            title: "评分成功！",
                            text: "你给了\""+movieName+"\""+$('#rating-input').val()+"星的评价！",
                            type: "success"
                        });
                        hasRate = true;
                    }
            }/*,
            error:function(XMLHttpRequest, textStatus, errorThrown){
                 alert(XMLHttpRequest.status);
                 alert(XMLHttpRequest.readyState);
                 alert(textStatus);
             }*/
         });

        }else if(hasRate){
            swal({
                title: "评分失败！",
                text: "你评过分了！",
                type: "error"
            });
        }else if(!window.sessionStorage.userId){
            swal({
                title: "评分失败！",
                text: "你还没登录！",
                type: "error"
            });
        }
    });

    var movieId = GetRequest();
    var url = baseURL+"/detail/?movie_id="+movieId;

    $('.btn.btn-white.btn-sm').click(function(){
        if(!window.sessionStorage.userId)
        swal({
                title: "未登录！",
                //text: "你给了\""+movieName+"\""+$('#rating-input').val()+"星的评价！",
                type: "error"
            });
        else{
            $.ajax({
        type:'get',
        url:baseURL+"/favor/?usr="+window.sessionStorage.userId+"&movie="+movieId,
        dataType:'jsonp',
        jsonp:'callback',
        jsonpCallback:"successCallback",
        success:function(data){
            console.log(data);
        }/*,
            error:function(XMLHttpRequest, textStatus, errorThrown){
                 alert(XMLHttpRequest.status);
                 alert(XMLHttpRequest.readyState);
                 alert(textStatus);
             }*/
         }); 
            swal({
                title: "收藏成功！",
                //text: "你给了\""+movieName+"\""+$('#rating-input').val()+"星的评价！",
                type: "success"
            });
        }
    });

    /*if(window.sessionStorage.userId){
        $.ajax({
        type:'get',
        url:baseURL+"/records/?usr="+window.sessionStorage.userId+"&movie="+movieId,
        dataType:'jsonp',
        jsonp:'callback',
        jsonpCallback:"successCallback",
        success:function(data){
            console.log(data);
        }/*,
            error:function(XMLHttpRequest, textStatus, errorThrown){
                 alert(XMLHttpRequest.status);
                 alert(XMLHttpRequest.readyState);
                 alert(textStatus);
             }*/
    //     }); 
    //}

    $.ajax({
        type:'get',
        url:url,
        dataType:'jsonp',
        jsonp:'callback',
        jsonpCallback:"successCallback",
        success:function(data){
            html = "";
            if((data.title).charAt(0) == '[')
                movieName = (data.title).slice(2,-2);
            else
                movieName = data.title;
            movieType = ((data.type).slice(1,-1)).replace(/ /g,"");

            tempType = movieType.split(',')
            formatMovieType = "";
            for(var i in tempType){
                formatMovieType += tempType[i].slice(1,-1);
                formatMovieType += '/';
            }
            formatMovieType = formatMovieType.slice(0,-1);
            
            movieCountry = data.ctr;
            movieLanguage = data.lan;
            movieTime = data.time;
            movieIntro = (data.intro=="" || data.intro=="[]")?"暂无简介...":data.intro;
            movieDir = data.dir==""?"暂无导演信息...":data.dir;
            movieBigPic = (data.big_pic).slice(2,-2);
            movieSmallPic = data.pic;
            movieDate = data.date==""?"暂无上映信息...":"上映日期:"+((data.date).slice(1,-1)).replace(/'/g,"");
            if(movieBigPic == "" && movieSmallPic == ""){
                picHtml = "<img src=\"img/movie_default_large.png\" class=\"carousel-inner img-responsive\">";                                
            } else if(movieSmallPic != ""){
                picHtml = "<div>"                                           
                +"<img src=\""+movieSmallPic+"\" class=\"carousel-inner img-responsive\">"                  
                +"</div>"
            }
            else
                {picHtml = "<div>"                                           
            +"<img src=\""+movieBigPic+"\" class=\"carousel-inner img-responsive\">"                  
            +"</div>"}
            $("#bigPicContainer").append(picHtml);
            $(".movieNameTitle").text("所有电影-"+movieName);
            $(".movieName").text(movieName);
            $(".movieDir").text(movieDir);
            $(".movieYear").text(movieDate);
            $(".movieIntro").text(movieIntro);
                /*                      <dt>电影编号</dt>
                                        <dd class="movieId"></dd>
                                        <dt>电影类型</dt>
                                        <dd class="movieType"></dd>
                                        <dt>制片国家</dt>
                                        <dd class="movieCountry"></dd>
                                        <dt>语言</dt>
                                        <dd class="movieLanguage"></dd>
                                        <dt>片长</dt>
                                        <dd class="movieLength"></dd>*/
                                        html += "<p>电影编号 : "+movieId+"</p>";
                                        if(movieType != "" )
                                            html += "<p>电影类型 : "+formatMovieType+"</p>";
                                        if(movieCountry != "")
                                            html += "<p>制片国家 : "+movieCountry+"</p>";
                                        if(movieLanguage != "")
                                            html += "<p>语言 : "+movieLanguage+"</p>";
                                        if(movieTime != "")
                                            html += "<p>片长 : "+movieTime+" 分钟</p>";
                                        $(".movieDetailedInfo").append(html);
                                        $.ajax({
                                            type:'get',
                                            url:baseURL+"/getItemRecMsg?movieTitle="+movieName,
                                            dataType:'jsonp',
                                            jsonp:'callback',
                                            jsonpCallback:"successCallback",
                                            success:function(data){
                                               for(var i in data){
                                                createAmovie(data[i].title,data[i].pic,data[i].intro,data[i].dir,data[i].id,data[i].type);
                                            }
                                        }
                                    }); 
                                    }
                                });



});