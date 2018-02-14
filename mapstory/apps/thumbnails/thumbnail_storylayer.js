var page = require('webpage').create();
var system = require('system');
var args = system.args;





//
//phantomjs --ignore-ssl-errors=true --web-security=false ol.pj thumnail_storylayer.html "https://docker/geoserver/geonode/wms" US_HistStateTerr_Gen0001_3aa6272c  -179.14736938476562  18.910842895507812 -66.9498291015625 71.38961791992188  ALL github.png
//


// Generate a thumbnail for a story layer
// This;
//  a) setup command line arguments
//  b) passes command line arguments to the webpage
//  c) waits until the webpage is ready for a screenshot (ready_for_screenshot=true)
//  d) waits for one second (to allow any wrapped (+180/-180) tiles to render)
//  e) saves the thumbnail


 
if (args.length != 11) {
  console.log('run with args: htmlFname wms layerName xmin ymin xmax ymax time output.fname quiet');
  phantom.exit(-1);
}  

  //parse from command line
  var htmlFname = args[1]
  var wms = args[2];
  var layerName = args[3].toLowerCase();
  var xmin = parseFloat(args[4]);
  var ymin = parseFloat(args[5]);
  var xmax = parseFloat(args[6]);
  var ymax = parseFloat(args[7]);
  var timeRange = args[8].toLowerCase();
  var outFname = args[9];
  var quiet = args[10].toLowerCase() == 'true';


  if (timeRange.toLowerCase() == "all")
    timeRange = '-99999999999-01-01T00:00:00.0Z/99999999999-01-01T00:00:00.0Z';

if (!quiet) {
   system.stderr.writeLine('wms = '+ wms);
   system.stderr.writeLine('layerName = '+ layerName);
   system.stderr.writeLine('xmin = '+ (xmin));
   system.stderr.writeLine('ymin = '+ (ymin));
   system.stderr.writeLine('xmax = '+ (xmax));
   system.stderr.writeLine('ymax = '+ (ymax));
   system.stderr.writeLine('timeRange = '+ timeRange);
   system.stderr.writeLine('outFname = '+ outFname);

   // add some debugging output  
  addDebugEvents(page,system);
}



  //open the HTML file and get ready to screen grab
  page.open(htmlFname, function() {                
               //get the map setup in the OL app
               page.evaluate(function(wms, layerName,xmin,ymin, xmax, ymax,time ) {
                                    setup(wms, layerName,xmin, ymin, xmax, ymax, time );
                             },wms,layerName,xmin,ymin, xmax, ymax,timeRange);

                // if it takes too long, hard close
                setTimeout(function() {
                    phantom.exit(666);
                }, 60000);
      
                //keep checking for ready_for_screenshot to be 1
  	            setInterval(function() {
                         //wait for ol to be ready to take a screen shot
                        var ready_for_screenshot = page.evaluate(function() {
                                return window.ready_for_screenshot;
                         });
                         // need to keep waiting?
      	                 if (!ready_for_screenshot)
                            return;
                         //page is up!
                         queueTakingSnapshot();       					   
        			    	}
  	 		      , 100);  //re-try every 100ms

   //unfortunately, OL does not have an easy way to determine
   // if the map is completely drawn.
   // when ready_for_screenshot become True, then the map is mostly
   // drawn -- but, there might be more rendering occuring if there is wrapping occuring
   // (i.e. 180/+180).  We wait 1 second for this rendering to occur.
   // NOTE: all the data is local, so this should just be drawing images - no remote data movement.
   function queueTakingSnapshot() {
      setTimeout(function () {
          takescreenshot();
      },1000);
    
   }
	  
   //take screenshot - determine the size/location of the map div and then take the screenshot
   function takescreenshot(){
          if (!quiet)
            system.stderr.writeLine('taking screenshot...');
          var clipRect = page.evaluate(function () {
                          var cr = document.querySelector("#map").getBoundingClientRect();
                          return cr;
                        });

          page.clipRect = {
                          top:    clipRect.top,
                          left:   clipRect.left,
                          width:  clipRect.width,
                          height: clipRect.height
                        };

          page.render(outFname,{format: 'png'}); 
          if (!quiet) 
            system.stderr.writeLine('done screenshot...');
          phantom.exit(0);//all done - quit with OK
   }

});



function addDebugEvents(page, system) {

  

   // page.onResourceRequested = function (request) {
   //     system.stderr.writeLine('onResourceRequested');
   //     system.stderr.writeLine('  +  url: ' + request.url);
  // };

   // page.onResourceReceived = function (response) {
   //    system.stderr.writeLine('onResourceReceived');
   //     system.stderr.writeLine('  url: ' + response.url);
   // };

  

  //  page.onNavigationRequested = function (url, type, willNavigate, main) {
  //      system.stderr.writeLine('onNavigationRequested');
  //      system.stderr.writeLine('  url: ' + url);
  //  };

  page.onConsoleMessage = function(msg) {
    console.log('CONSOLE: ' + msg  );
  };

    page.onResourceError = function (resourceError) {
        system.stderr.writeLine('onResourceError');
        system.stderr.writeLine('  error: ' + resourceError.errorString);
        system.stderr.writeLine('  url: ' + resourceError.url);
    };

    page.onResourceError = function (resourceError) {
        system.stderr.writeLine('onResourceError');
        system.stderr.writeLine('  - url: ' + resourceError.url);
        system.stderr.writeLine('  - errorCode: ' + resourceError.errorCode);
        system.stderr.writeLine('  - errorString: ' + resourceError.errorString);
    };

 // from http://phantomjs.org/api/phantom/handler/on-error.html
    page.onError = function (msg, trace) {
       var msgStack = ['PHANTOM ERROR: ' + msg];

       if (trace && trace.length) {
          msgStack.push('TRACE:');
          trace.forEach(function(t) {
            msgStack.push(' -> ' + (t.file || t.sourceURL) + ': ' + t.line + (t.function ? ' (in function ' + t.function +')' : ''));
          });
        }
        console.log(msgStack.join('\n'));
    };

}