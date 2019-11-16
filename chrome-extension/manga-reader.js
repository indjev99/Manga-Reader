// content.js

var images = document.getElementsByTagName('img');

var sources = [];
for(let i = 0; i < images.length; i++)
{
    sources.push(images[i].src);
}
console.log(sources);

var currImage = -1;
for(let i = 0; i < images.length; i++)
{
    images[i].addEventListener('mouseover', function()
    {
        currImage = i;
    })
    images[i].addEventListener('mouseout', function()
    {
        currImage = -1;
    })
}

document.onmousemove = function(e)
{
    if (currImage >= 0)
    {
        var x = e.pageX;
        var y = e.pageY;
    
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

        console.log("id = " + currImage + " x = " + imageX + " y = " + imageY);
    }
}