// content.js

const minMoveDist = 15;
const waitTime = 400;

var images = [];
var sources = [];
var lastImage = -1;
var lastX = 0;
var lastY = 0;
var message = null;
var initialized = false;

function updateImages(e)
{
    var newImages = document.getElementsByTagName('img');
    var newSources = [];
    var sizes = [];
    for(let i = 0; i < newImages.length; i++)
    {
        sizes.push({
            'w' : newImages[i].naturalWidth,
            'h' : newImages[i].naturalHeight});
        newSources.push(newImages[i].src);
    }

    var different = false;
    if (sources.length != newSources.length) different = true;
    for (let i = 0; i < sources.length && !different; i++)
    {
        if (sources[i] != newSources[i]) different = true;
    }
    if (!different) return;

    images = newImages;
    sources = newSources;
    lastImage = -1;
    message = null;
    initialized = false;

    var init_message = {'image_urls' : sources, 'image_sizes' : sizes};
    $.post('http://localhost:5000/init_images_request', JSON.stringify(init_message), function(data) { initialized = true; });
}
updateImages(null);

document.onclick = updateImages;

document.onmousemove = function(e)
{
    var x = e.pageX;
    var y = e.pageY;
    var pageRect = document.body.getBoundingClientRect();
    x += pageRect.left;
    y += pageRect.top;

    var currImage = -1;

    for (let i = 0; i < images.length && currImage == -1; i++)
    {
        var rect = images[i].getBoundingClientRect();

        var left = rect.left;
        var right = rect.right;

        var top = rect.top ;
        var bottom = rect.bottom;

        var imageX = (x - left) / (right - left);
        var imageY = (y - top) / (bottom - top);

        if (imageX >= 0 && imageX <= 1 && imageY >=0 && imageY <= 1) currImage = i;
    }

    if (currImage >= 0)
    {
        var dist = (x - lastX) * (x - lastX) + (y - lastY) * (y - lastY);
        if (lastImage == currImage && dist < minMoveDist * minMoveDist) return;

        lastImage = currImage;
        lastX = x;
        lastY = y;

        message = {'id' : currImage, 'x' : imageX, 'y' : imageY};
    }
}

var wait = setInterval(function()
{
    if (message && initialized)
    {
        $.post('http://localhost:5000/register_mouse_request', JSON.stringify(message));
        message = null;
    }
}, waitTime);

document.onkeypress = function(e)
{
    if (e.key == 'e' || e.key == 'E')
    {
        $.post('http://localhost:5000/set_output_language_request', JSON.stringify('en'));
    }
    if (e.key == 'j' || e.key == 'J')
    {
        $.post('http://localhost:5000/set_output_language_request', JSON.stringify('ja'));
    }
}