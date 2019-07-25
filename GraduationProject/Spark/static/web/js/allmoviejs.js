
$(document).ready(function(){
    typeArray = new Array();
    selectCtr = -1;
    selectType = -1;
    currentPage = 1;
    totalPage = 1;
    baseURL = "http://118.25.122.180:8000";
    function createAmovie(movieName,moviePic,movieIntro,movieDir,movieID,movieType){
        movieIntr = movieIntro.length>100?movieIntro.substring(0,100)+"...":movieIntro;
        if(movieIntro == "[]"){
            movieIntr = "暂无简介...";   
        }
        movieTp = (movieType.slice(1,-1)).replace(/ /g,"");
        if((movieName).charAt(0) == '[')
            movieName = (movieName).slice(2,-2);
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
        +"<a id=\""+movieID+"\" href=\"single_movie_detail.html?id="+movieID+"\" class=\"text-navy\">"
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
        var recordurl = "http://118.25.122.180:8000";
        if(window.sessionStorage.userId){
            $("a#"+movieID).click(function(){
                $.get(recordurl+"/records/?movie="+movieID+"&usr="+window.sessionStorage.userId, function(result){
                    console.log(result);
                });
            });
        }
    };

    $.ajax({
        type:'get',
        url:baseURL+'/all?ctr=-1&type=-1&page=1',
        dataType:'jsonp',
        jsonp:'callback',
        jsonpCallback:"successCallback",

        success:function(data){
            arr = new Array();
            arr = data.movie_info;

            no = 0;
            html = "";
            for(var i in arr){
                createAmovie(arr[i].movie_title,arr[i].movie_pic,arr[i].movie_intro,arr[i].movie_dir,arr[i].movie_id,arr[i].movie_type);
            }
            totalPage = Math.ceil(data.movie_num/10);;
            pageNavObj = new PageNavCreate("PageNavId",{
                pageCount:totalPage,//总页数
                currentPage:1,//当前页
                perPageNum:5,//每页按钮数
            });
            pageNavObj.afterClick(pageNavCallBack);

            }/*,
            error:function(XMLHttpRequest, textStatus, errorThrown){
                 alert(XMLHttpRequest.status);
                 alert(XMLHttpRequest.readyState);
                 alert(textStatus);
             }*/
         }); 

    

    $(".select2_demo_2").select2({
        placeholder: "选择一个或几个类型",
        allowClear: true,
        maximumSelectionLength :3,
        templateSelection: function(repo){
            if(repo.text == "选择一个或几个类型")
                selectType = "-1";
            else{
                selectType += repo.text;
            }

            return repo.text;}
        });

    $(".select2_demo_3").select2({
        placeholder: "选择一个国家/地区",
        allowClear: true,
        templateSelection: function(repo){
            selectCtr = "";
            if(repo.text == "选择一个国家/地区")
                selectCtr = "-1";
            else{
                selectCtr = repo.text;
            }
            return repo.text;}
        });
    function getPageSet(){
        var obj = {
                pageCount:null,//总页数
                currentPage:null,//当前页
                perPageNum:null,//每页按钮数
            }
            if($("#testPageCount").val() && !isNaN(parseInt($("#testPageCount").val()))){
                obj.pageCount = parseInt($("#testPageCount").val());
            }else{
                obj.pageCount = parseInt($(".page-input-box > input").attr("placeholder"));
            }

            if($("#testCurrentPage").val() && !isNaN(parseInt($("#testCurrentPage").val()))){
                obj.currentPage = parseInt($("#testCurrentPage").val());
                obj.currentPage = (obj.currentPage<=obj.pageCount ? obj.currentPage : obj.pageCount);
            }else{
                obj.currentPage = 1;
            }
            if($("#testPerPageNum").val() && !isNaN(parseInt($("#testPerPageNum").val()))){
                obj.perPageNum = parseInt($("#testPerPageNum").val());
            }else{
                obj.perPageNum = null;
            }
            return obj;
        }


       /* pageNavObj = new PageNavCreate("PageNavId",{
                pageCount:160,//总页数
                currentPage:1,//当前页
                perPageNum:5,//每页按钮数
            });*/


            function pageNavCallBack(clickPage){
            //clickPage是被点击的目标页码
            //console.log(clickPage);
            currentPage = clickPage;

            //一般来说可以在这里通过clickPage,执行AJAX请求取数来重写页面
            $.ajax({
                type:'get',
                url:baseURL+"/all?ctr="+selectCtr+"&type="+selectType+"&page="+currentPage,
                dataType:'jsonp',
                jsonp:'callback',
                jsonpCallback:"successCallback",

                success:function(data){
                    arr = new Array();
                    arr = data.movie_info;
                    no = 0;
                    html = "";
                    $(".movieContainer").empty();
                    for(var i in arr){
                        createAmovie(arr[i].movie_title,arr[i].movie_pic,arr[i].movie_intro,arr[i].movie_dir,arr[i].movie_id,arr[i].movie_type);
                    }
                    totalPage = Math.ceil(data.movie_num/10);          
            }/*,
            error:function(XMLHttpRequest, textStatus, errorThrown){
                 alert(XMLHttpRequest.status);
                 alert(XMLHttpRequest.readyState);
                 alert(textStatus);
             }*/
         }); 


            //最后别忘了更新一遍翻页导航栏
            //pageNavCreate("PageNav",pageCount,clickPage,pageNavCallBack);
            pageNavObj = new PageNavCreate("PageNavId",{
                pageCount:totalPage,//总页数
                currentPage:clickPage,//当前页
                perPageNum:getPageSet().perPageNum,//每页按钮数
            });
            pageNavObj.afterClick(pageNavCallBack);
        }


        //pageNavObj.afterClick(pageNavCallBack);

        $(".btn-success").click(function(){
            ctr = $(".select2_demo_3").select2('val');
            if(ctr == null){
                ctr = -1;
            }
            selectCtr = ctr;
            arr = new Array();
            arr = $(".select2_demo_2").select2('val');
            type = "";
            if(arr == null){
                type = -1;
            }else{
                for(var i in arr){
                    type += arr[i];
                    type += "+";
                }
                type = type.slice(0,-1);
            }
            selectType = type;
            
            currentPage = 1; 
            $.ajax({
                type:'get',
                url:baseURL+"/all?ctr="+selectCtr+"&type="+selectType+"&page="+currentPage,
                dataType:'jsonp',
                jsonp:'callback',
                jsonpCallback:"successCallback",

                success:function(data){
                    arr = new Array();
                    arr = data.movie_info;
                    no = 0;
                    html = "";
                    $(".movieContainer").empty();
                    for(var i in arr){
                        createAmovie(arr[i].movie_title,arr[i].movie_pic,arr[i].movie_intro,arr[i].movie_dir,arr[i].movie_id,arr[i].movie_type);
                    }
                    totalPage = Math.ceil(data.movie_num/10);
                    pageNavObj = new PageNavCreate("PageNavId",{
                pageCount:totalPage,//总页数
                currentPage:currentPage,//当前页
                perPageNum:getPageSet().perPageNum,//每页按钮数
            });
                    pageNavObj.afterClick(pageNavCallBack);             
            }/*,
            error:function(XMLHttpRequest, textStatus, errorThrown){
                 alert(XMLHttpRequest.status);
                 alert(XMLHttpRequest.readyState);
                 alert(textStatus);
             }*/
         });

        });


        
    });
