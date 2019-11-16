// content.js

var images = document.getElementsByTagName('img');

var sources = [];
var currImage = -1;
for(let i = 0; i < images.length; i++)
{
    sources.push(images[i].src);
    images[i].addEventListener('mouseover', function()
    {
        currImage = i;
    })
    images[i].addEventListener('mouseout', function()
    {
        currImage = -1;
    })
}
$.post('http://localhost:5000/init_images', JSON.stringify(sources));


var minMoveDist = 30;
var lastX = 0;
var lastY = 0;
var lastImage = -1;
var waitTime = 250;
var message = null;
document.onmousemove = function(e)
{
    if (currImage >= 0)
    {
        var x = e.pageX;
        var y = e.pageY;

        var dist = (x - lastX) * (x - lastX) + (y - lastY) * (y - lastY);

        if (lastImage != currImage && dist < minMoveDist * minMoveDist) return;

        lastX = x;
        lastY = y;
        lastImage = currImage;

        var rect = images[currImage].getBoundingClientRect();
        var pageRect = document.body.getBoundingClientRect();

        var left = rect.left - pageRect.left;
        var right = rect.right - pageRect.left;

        var top = rect.top - pageRect.top;
        var bottom = rect.bottom - pageRect.top;

        var imageX = (x - left) / (right - left);
        var imageY = (y - top) / (bottom - top);

        if (imageX < 0) imageX = 0;
        if (imageX > 1) imageX = 1;

        if (imageY < 0) imageY = 0;
        if (imageY > 1) imageY = 1;

        message = {'id' : currImage, 'x' : imageX, 'y' : imageY};
    }
}

var wait = setInterval(function(){
    if (message)
    {
        $.post('http://localhost:5000/register_mouse', JSON.stringify(message));
        message = null;
    }
}, waitTime);