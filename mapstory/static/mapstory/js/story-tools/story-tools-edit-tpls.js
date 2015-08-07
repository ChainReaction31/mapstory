angular.module("storytools.edit.templates", []).run(["$templateCache", function($templateCache) {$templateCache.put("boxes/bounds-editor.html","<div class=row><div class=\"box-bounds-map col-lg-6\" style=height:15em;></div><div class=col-md-3><div class=form-group><label for=minlon>Min. Longitude:</label> <input type=text class=form-control id=minlon ng-model=storyBox.minlon placeholder=\"Min. Longitude\" value=0.0></div><div class=form-group><label for=minlat>Min. Latitude:</label> <input type=text class=form-control id=minlat ng-model=storyBox.minlat placeholder=\"Min. Latitude\" value=0.0></div><div class=form-group><label for=zoomLevel>Zoom Level</label> <input class=\"col-sm-12 form-control\" ng-model=storyBox.zoom id=zoomLevel type=number placeholder=\"Zoom Level\"></div></div><div class=col-md-3><div class=form-group><label for=maxlon>Max. Longitude:</label> <input type=text class=form-control ng-model=storyBox.maxlon id=maxlon placeholder=\"Max. Longitude\" value=0.0></div><div class=form-group><label for=maxlat>Max. Latitude:</label> <input type=text class=form-control ng-model=storyBox.maxlat id=maxlat placeholder=\"Max. Latitude\" value=0.0></div></div></div><button class=\"btn btn-default\" ng-click=updateCoordinates();>Use Current Map Bounds</button> <button class=\"btn btn-default\" ng-click=updateCoordinates(true);>Use Bounds of Selected Layers</button>");
$templateCache.put("boxes/box-chooser.html","<div><button class=\"btn btn-default pull-right\" ng-click=boxesCtrl.newStoryBox();>Add a StoryBox</button><table class=\"table table-condensed\"><thead><tr><th>Title</th><th>Start Time</th><th>End Time</th><th>Delete</th></tr></thead><tbody><tr ng-class=\"boxesCtrl.editingCopy == box ? \'active\' : \'\'\" ng-repeat=\"box in boxesCtrl.StoryBoxLayerManager.storyBoxes\"><td ng-click=boxesCtrl.editStoryBox(box) style=\"cursor: pointer;\">{{ box.title }}</td><td>{{ box.start_time|isodate }}</td><td>{{ box.end_time|isodate }}</td><td><i ng-click=boxesCtrl.deleteStoryBox(box) style=\"cursor: pointer;\" class=\"glyphicon glyphicon-trash\"></i></td></tr></tbody></table></div>");
$templateCache.put("boxes/box-editor-form.html","<form name=boxForm class=form><div ng-if=boxesCtrl.editingBox><tabset ng-init=\"boxBoundsEditorSelected = false\" class=clearfix><tab heading=Contents><div class=col-lg-4><div class=form-group><label for=title>Title</label> <input ng-model=storyBox.title ng-required=true class=form-control id=title name=title placeholder=Title> <span ng-show=boxForm.title.$error.required>Box Title is Required</span></div><div class=form-group><label for=description>Description</label> <textarea ng-model=storyBox.description class=form-control id=description placeholder=Description></textarea></div></div><div class=col-lg-4><div class=form-group><label for=start_time>Start Time</label><st-date-time-field date-time=storyBox.start_time></st-date-time-field></div><div class=form-group><label for=playbackRate>Playback Rate</label> <input type=number ng-model=storyBox.playback ng-init=\"storyBox.playback=3\" class=form-control id=playbackRate><select ng-model=storyBox.playbackRate ng-init=\"storyBox.playbackRate=\'seconds\'\" class=form-control><option value=seconds>Seconds</option><option value=minutes>Minutes</option></select></div></div><div class=col-lg-4><div class=form-group><label for=end_time>End Time</label><st-date-time-field date-time=storyBox.end_time></st-date-time-field></div><div ng-if=boxForm.$error.range class=ng-invalid>Start must be before End</div><div class=form-group><label for=timestep>Timestep</label> <input ng-model=storyBox.interval ng-init=\"storyBox.interval=1\" type=number class=form-control id=timestep><select ng-model=storyBox.intervalRate ng-init=\"storyBox.intervalRate=\'years\'\" class=form-control><option value=minutes>Minutes</option><option value=hours>Hours</option><option value=weeks>Weeks</option><option value=months>Months</option><option value=years>Years</option></select></div></div></tab><tab heading=Bounds select=\"boxBoundsEditorSelected = true\" deselect=\"boxBoundsEditorSelected = false\"><box-bounds-editor class=container selected=boxBoundsEditorSelected></box-bounds-editor></tab><tab heading=Layers><box-layers-editor></box-layers-editor></tab></tabset><button class=\"btn btn-primary\" ng-disabled=!boxCtrl.isFormValid() ng-click=boxesCtrl.acceptEdit()>Save</button> <button class=\"btn btn-primary\" ng-click=boxesCtrl.cancelEdit()>Cancel</button></div></form>");
$templateCache.put("boxes/box-editor.html","<form name=boxForm class=form><div ng-if=boxesCtrl.editingBox><tabset ng-init=\"boxBoundsEditorSelected = false\" class=clearfix><tab heading=Contents><box-contents-editor class=container></box-contents-editor></tab><tab heading=Bounds select=\"boxBoundsEditorSelected = true\" deselect=\"boxBoundsEditorSelected = false\"><box-bounds-editor selected=boxBoundsEditorSelected class=container></box-bounds-editor></tab><tab heading=Layers><box-layers-editor class=container></box-layers-editor></tab></tabset><div class=pull-right><button class=\"btn btn-primary\" ng-disabled=!boxCtrl.isFormValid() ng-click=boxesCtrl.saveStoryBox()>Save</button> <button class=\"btn btn-primary\" ng-click=boxesCtrl.cancelEdit()>Cancel</button></div></div></form>");
$templateCache.put("boxes/contents-editor.html","<div class=col-lg-4><div class=form-group><label for=title>Title</label> <input tabindex=0 ng-model=storyBox.title ng-required=true class=form-control id=title name=title placeholder=Title> <span ng-if=boxForm.title.$error.required class=ng-invalid>Box Title is Required</span></div><div class=form-group><label for=description>Description</label> <textarea tabindex=1 ng-model=storyBox.description class=form-control id=description placeholder=Description></textarea></div></div><div class=col-lg-4><div class=form-group><label for=start_time>Start Time</label><st-date-time-field date-time=storyBox.start_time></st-date-time-field></div><div class=form-group><label for=playbackRate>Playback Rate</label> <input tabindex=4 type=number ng-model=storyBox.playback ng-init=\"storyBox.playback=3\" class=form-control id=playbackRate><select tabindex=5 ng-model=storyBox.playbackRate ng-init=\"storyBox.playbackRate=\'seconds\'\" class=form-control><option value=seconds>Seconds</option><option value=minutes>Minutes</option></select></div></div><div class=col-lg-4><div class=form-group><label for=end_time>End Time</label><st-date-time-field date-time=storyBox.end_time></st-date-time-field><span ng-if=boxForm.$error.range class=ng-invalid>Start must be before End</span></div><div class=form-group><label for=timestep>Timestep</label> <input tabindex=6 ng-model=storyBox.interval ng-init=\"storyBox.interval=1\" type=number class=form-control id=timestep><select tabindex=7 ng-model=storyBox.intervalRate ng-init=\"storyBox.intervalRate=\'years\'\" class=form-control><option value=minutes>Minutes</option><option value=hours>Hours</option><option value=weeks>Weeks</option><option value=months>Months</option><option value=years>Years</option></select></div></div>");
$templateCache.put("boxes/layers-editor.html","<table class=\"table table-striped\"><thead><tr><th></th><th>Layer Name</th><th>Type</th><th>Author</th><th></th></tr></thead><tbody><tr ng-repeat=\"layer in mapManager.storyMap.getStoryLayers().getArray()\"><th scope=row><button type=button data-toggle=button ng-click=\"mapManager.storyMap.toggleVisibleLayer(layer); $event.stopPropagation();\" class=\"btn btn-xs btn-default\"><i class=glyphicon ng-class=\"{\'glyphicon-eye-open\': layer.get(\'visibility\'), \'glyphicon-eye-close\': !layer.get(\'visibility\')}\"></i></button></th><td>{{layer.get(\'title\')}}</td><td>{{layer.get(\'type\')}}</td><td>{{layer.get(\'owner\')}}</td><td><button type=button data-toggle=button ng-click=\"mapManager.storyMap.removeLayer(layer); $event.stopPropagation();\" class=\"btn btn-xs btn-default\"><i class=\"glyphicon glyphicon-trash\"></i></button></td></tr></tbody></table>");
$templateCache.put("pins/pin-chooser.html","<div><table class=\"table table-condensed\"><thead><tr><th></th><th>Title</th><th>Start Time</th><th>End Time</th><th>Geometry</th><th>In Map</th><th>In Timeline</th><th></th></tr></thead><tbody><tr ng-repeat=\"pin in pinsCtrl.StoryPinLayerManager.storyPins\" ng-class=\"pinsCtrl.currentPin == pin ? \'active\' : \'\'\"><td><i ng-click=editPin(pin) style=\"cursor: pointer;\" class=\"glyphicon glyphicon-edit\"></i></td><td>{{ pin.title }}</td><td>{{ pin.start_time|isodate }}</td><td>{{ pin.end_time|isodate }}</td><td>{{ pin.getGeometry().getType() }}</td><td>{{ pin.in_map }}</td><td>{{ pin.in_timeline }}</td><td><i ng-click=pinsCtrl.deleteStoryPin(pin) style=\"cursor: pointer;\" class=\"glyphicon glyphicon-trash\"></i></td></tr></tbody></table></div>");
$templateCache.put("pins/pin-editor-form.html","<form name=pinForm class=\"form form-horizontal pin-editor-form\"><div class=form-group><label for=storyPinTitle>StoryPin Title</label> <input name=title ng-required=true ng-model=storyPin.title class=form-control type=text id=storyPinTitle placeholder=Title></div><div class=form-group><label for=storyPinAbstract>Content</label> <textarea ng-model=storyPin.content id=storyPinAbstract class=form-control rows=2 placeholder=Content></textarea></div><hr><div class=form-group><label>Location</label><div><div class=\"btn-group nopad\"><button class=btn ng-model=pinsCtrl.activeDrawTool btn-radio=\"\'Point\'\">Point</button> <button class=btn ng-model=pinsCtrl.activeDrawTool btn-radio=\"\'LineString\'\">Line</button> <button class=btn ng-model=pinsCtrl.activeDrawTool btn-radio=\"\'Polygon\'\">Polygon</button></div><div ng-if=storyPin.getGeometry() class=\"btn-group nopad pull-right\"><button class=btn ng-class=\"pinsCtrl.activeDrawTool == \'Modify\' ? \'active\' : null\" ng-click=\"pinsCtrl.activeDrawTool = \'Modify\'\">Edit</button> <button class=btn ng-click=pinsCtrl.deleteGeometry()>Delete</button></div></div></div><hr><div class=form-group><label>Start Time</label><st-date-time-field date-time=storyPin.start_time></st-date-time-field></div><div class=form-group><label>End Time</label><st-date-time-field date-time=storyPin.end_time></st-date-time-field></div><div ng-if=pinForm.$error.range class=ng-invalid>Start must be before End</div><table ng-if=showPointCoordinates() class=\"table table-bordered table-condensed table-hover\" style=\"background-color: white\"><tbody><tr><td>Latitude</td><td><input ng-model=point.latitude class=form-control type=number placeholder=DD.MMSSSS></td></tr><tr><td>Longitude</td><td><input ng-model=point.longitude class=form-control type=number placeholder=DD.MMSSSS></td></tr></tbody></table><hr><div class=form-group><label>Options</label><div><div class=checkbox><input ng-model=storyPin.in_timeline id=showInTimeline type=checkbox> <label for=showInTimeline>Show in Timeline</label></div><div class=checkbox><input ng-model=storyPin.in_map id=showInMap type=checkbox> <label for=showInMap>Show in Map</label></div></div></div></form>");
$templateCache.put("style/rules-editor.html","<div class=style-editor-item><div class=title>Rules</div><table class=controls><tbody><tr ng-repeat=\"rule in activeStyle.rules\" class=style-rule><td>{{ rule.name}}</td><td><color-editor st-model=rule.style.symbol property=fillColor ng-if=rule.style.symbol.fillColor></color-editor><color-editor st-model=rule.style.stroke property=strokeColor ng-if=rule.style.stroke.strokeColor></color-editor><number-editor st-model=rule.style.symbol property=size ng-if=\"rule.style.symbol.size != null\"></number-editor></td><td><button ng-click=deleteRule(rule)>&times;</button></td></tr></tbody></table></div>");
$templateCache.put("style/style-editor.html","<form name=editorForm class=well><div class=style-type-header><div class=btn-group data-dropdown><button type=button class=\"btn btn-primary dropdown-toggle\">Style: {{currentEditor.displayName}}<span class=caret></span></button><ul class=dropdown-menu role=menu><li ng-repeat=\"styleType in styleTypes\" ng-click=setActiveStyle(styleType)>{{styleType.displayName}}</li></ul></div></div><div><style-type-editor ng-if=layer></style-type-editor><rules-editor ng-if=activeStyle.rules></rules-editor></div></form>");
$templateCache.put("time/date-time-field.html","<div class=input-group><input type=text iso-date-time class=form-control ng-model=dateTime placeholder=YYYY-MM-DDTHH:mm:ss> <span class=input-group-btn><button ng-click=setFromCurrentTime() title=\"Set From Current Time\"><i class=\"glyphicon glyphicon-time\"></i></button></span></div>");
$templateCache.put("style/types/class-point.html","<classify-editor attribute-filter=number show-method=true show-max-classes=true show-color-ramp=true></classify-editor><symbol-editor hide-color=true st-model=activeStyle show-graphic=true show-rotation=true></symbol-editor><stroke-editor st-model=activeStyle></stroke-editor><label-editor st-model=activeStyle></label-editor>");
$templateCache.put("style/types/class-polygon.html","<classify-editor attribute-filter=number show-method=true show-max-classes=true show-color-ramp=true></classify-editor><stroke-editor st-model=activeStyle></stroke-editor><label-editor st-model=activeStyle></label-editor>");
$templateCache.put("style/types/graduated-point.html","<classify-editor attribute-filter=number show-method=true show-color-ramp=false show-max-classes=true show-range=true show-rotation=true></classify-editor><stroke-editor st-model=activeStyle></stroke-editor><label-editor st-model=activeStyle></label-editor>");
$templateCache.put("style/types/heatmap.html","<div class=style-editor-item><div class=title>Radius</div><div class=controls><number-editor st-model=activeStyle property=radius max=64></number-editor></div><div class=title>Opacity</div><div class=controls><number-editor st-model=activeStyle property=opacity min=0 step=.1 max=1></number-editor></div></div>");
$templateCache.put("style/types/simple-line.html","<stroke-editor st-model=activeStyle></stroke-editor><label-editor st-model=activeStyle></label-editor>");
$templateCache.put("style/types/simple-point.html","<symbol-editor st-model=activeStyle show-graphic=true show-rotation=true></symbol-editor><stroke-editor st-model=activeStyle></stroke-editor><label-editor st-model=activeStyle></label-editor>");
$templateCache.put("style/types/simple-polygon.html","<symbol-editor st-model=activeStyle></symbol-editor><stroke-editor st-model=activeStyle></stroke-editor><label-editor st-model=activeStyle></label-editor>");
$templateCache.put("style/types/unique-line.html","<classify-editor attribute-filter=unique show-method=false show-max-classes=true show-color-palette=true></classify-editor><stroke-editor st-model=activeStyle></stroke-editor><label-editor st-model=activeStyle></label-editor>");
$templateCache.put("style/types/unique-point.html","<classify-editor attribute-filter=unique show-method=false show-max-classes=true show-color-palette=true show-rotation=true></classify-editor><symbol-editor hide-color=true st-model=activeStyle show-graphic=true show-rotation=true></symbol-editor><stroke-editor st-model=activeStyle></stroke-editor><label-editor st-model=activeStyle></label-editor>");
$templateCache.put("style/types/unique-polygon.html","<classify-editor attribute-filter=unique show-method=false show-max-classes=true show-color-palette=true></classify-editor><stroke-editor st-model=activeStyle></stroke-editor><label-editor st-model=activeStyle></label-editor>");
$templateCache.put("style/widgets/attribute-combo.html","<div data-dropdown><button type=button class=dropdown-toggle>{{model[property]||\'Select Attribute\'}}<span class=caret></span></button><ul class=\"dropdown-menu scrollable-combo {{css}}\" role=menu><li ng-click=\"onChange(property, null)\">[ None ]</li><li ng-repeat=\"attribute in attributes\" ng-click=\"onChange(property, attribute)\">{{attribute}}</li></ul></div>");
$templateCache.put("style/widgets/classify-editor.html","<div class=style-editor-item><div class=title>Classification</div><div class=controls><attribute-combo filter={{attributeFilter}} on-change=changeClassifyProperty layer=layer st-model=activeStyle.classify css=classify-attribute></attribute-combo><div class=btn-group ng-if=showMaxClasses><input class=btn-xs size=3 type=number min=2 step=1 max=9 ng-model=activeStyle.classify.maxClasses ng-change=changeClassifyProperty()></div><div class=btn-group ng-if=showFixedClasses><button class=btn ng-model=radioModel btn-radio=3>3</button> <button class=btn ng-model=radioModel btn-radio=5>5</button> <button class=btn ng-model=radioModel btn-radio=7>7</button></div></div><div class=controls><div class=btn-group data-dropdown ng-if=showColorRamp><button type=button class=dropdown-toggle><canvas data-color-ramp width=200 height=14 data-ramp=activeStyle.classify.colorRamp ng-if=activeStyle.classify.colorRamp></canvas><span ng-if=\"activeStyle.classify.colorRamp == null\">Color Ramp</span> <span class=caret></span></button><ul class=dropdown-menu role=menu><li ng-click=\"activeStyle.classify.colorRamp=null\">[ None ]</li><li ng-repeat=\"ramp in styleChoices.colorRamps\" ng-click=\"changeClassifyProperty(\'colorRamp\',ramp)\"><canvas data-color-ramp width=200 height=14 data-ramp=ramp></canvas></li></ul></div><div class=btn-group data-dropdown ng-if=showColorPalette><button type=button class=dropdown-toggle><span>{{ activeStyle.classify.colorPalette||\'Color Palette\'}}</span> <span class=caret></span></button><ul class=dropdown-menu role=menu><li ng-click=\"activeStyle.classify.colorPalette=null\">[ None ]</li><li class=clearfix ng-repeat=\"p in styleChoices.colorPalettes\" ng-click=\"changeClassifyProperty(\'colorPalette\',p.name)\"><div>{{ p.name }}</div><div class=color-square ng-repeat=\"c in p.vals\" style=\"background-color: {{ c }}\"></div></li></ul></div><div class=btn-group dropdown ng-if=showMethod><button type=button class=dropdown-toggle>{{activeStyle.classify.method || \'Method\'}}<span class=caret></span></button><ul class=dropdown-menu role=menu><li ng-repeat=\"method in styleChoices.classMethods\" ng-click=\"changeClassifyProperty(\'method\',method)\"><span>{{method}}</span></li></ul></div></div><div class=controls ng-if=showRange><div data-dropdown><button type=button class=dropdown-toggle>{{activeStyle.classify.range.min}} - {{activeStyle.classify.range.max}}<span class=caret></span></button><div class=dropdown-menu role=menu><label>Min:</label><input no-close size=3 name=classifyRangeMin type=number min=0 max={{activeStyle.classify.range.max}} ng-model=activeStyle.classify.range.min ng-change=changeClassifyProperty><br><label>Max:</label><input no-close size=3 name=classifyRangeMax type=number min={{activeStyle.classify.range.min}} max=200 ng-model=activeStyle.classify.range.max ng-change=changeClassifyProperty></div></div></div></div>");
$templateCache.put("style/widgets/color-editor.html","<div class=btn-group data-dropdown><button type=button class=dropdown-toggle><i ng-style=\"{\'backgroundColor\': stModel[property]}\" class=color-picker>&nbsp; &nbsp; &nbsp;</i> <span class=caret></span></button><ul no-close class=\"dropdown-menu color-select\" role=menu><input color-field ng-model=stModel[property]><div no-close colorpicker colorpicker-parent=true colorpicker-position=bottom type=button ng-model=stModel[property]></div></ul></div>");
$templateCache.put("style/widgets/graphic-editor.html","<div data-dropdown><button type=button class=dropdown-toggle><span data-current-symbol></span> <span class=caret></span></button><div class=\"dropdown-menu symbol-selector\" role=menu><div>Marks</div><div class=ol-marks></div><div ng-if=recent>Recent Icons</div><div class=recent-icons></div><button class=\"btn btn-small\" ng-click=showIconCommons()>Icon Commons</button></div></div>");
$templateCache.put("style/widgets/icon-commons-search.html","<div class=modal-header><h3 class=modal-title>Icon Commons</h3></div><div class=\"modal-body icon-commons-search\"><tabset type=pills><tab heading=Collections select=viewCollections()><input ng-model=_typeAhead type=text placeholder=\"Search By Collection\" typeahead=\"c.name for c in collections | filter:$viewValue | limitTo:10\" class=form-control typeahead-on-select=\"collectionSelect($item, $model, $label)\"></tab><tab heading=Search select=viewTags()><input ng-model=_typeAhead type=text placeholder=\"Search By Tag\" typeahead-wait-ms=250 typeahead=\"tag for tag in getTags($viewValue)\" class=form-control typeahead-on-select=\"tagSelect($item, $model, $label)\"></tab></tabset><div class=\"clearfix icon-list\"><ul ng-if=icons><li ng-repeat=\"i in icons._icons\" ng-class=selectedClass(i)><img title={{i.name}} ng-src={{i.href}} ng-click=iconSelected(i) ng-dblclick=\"iconSelected(i, true)\"></li></ul></div><button ng-if=icons._more ng-click=loadMore() class=\"col-lg-4 col-lg-offset-4 btn btn-primary\">Load More</button></div><div class=modal-footer><button class=\"btn btn-primary\" ng-click=close()>OK</button> <button class=btn ng-click=dismiss()>Cancel</button></div>");
$templateCache.put("style/widgets/label-editor.html","<div ng-form=label class=style-editor-item><div class=title>Label</div><div class=controls><attribute-combo layer=layer st-model=model css=label-attribute filter=nogeom></attribute-combo><number-editor st-model=model property=fontSize></number-editor></div><div class=controls><div dropdown><button type=button class=dropdown-toggle>{{model.fontFamily}} <span class=caret></span></button><ul class=\"dropdown-menu scrollable-combo font-family\" role=menu><li ng-repeat=\"family in styleChoices.fontFamily\" ng-click=\"model.fontFamily=family\">{{family}}</li></ul></div><color-editor st-model=model property=fillColor></color-editor><div class=btn-group><button class=btn ng-model=styleModel.bold btn-checkbox ng-change=styleModelChange()><strong>B</strong></button> <button class=btn ng-model=styleModel.underline ng-change=styleModelChange()><u>U</u></button> <button class=btn ng-model=styleModel.italic btn-checkbox ng-change=styleModelChange()><i>I</i></button> <button class=btn ng-model=styleModel.halo ng-change=styleModelChange()>H</button> <button class=btn ng-model=styleModel.shadow ng-change=styleModelChange()>S</button></div></div></div>");
$templateCache.put("style/widgets/number-editor.html","<div data-dropdown><button type=button class=dropdown-toggle>{{stModel[property]||\'number\'}} <span class=caret></span></button><div class=dropdown-menu role=menu><input no-close size=3 type=number min={{min}} max={{max}} step={{step}} value=10 name=\"{{ property }}\" ng-model=stModel[property]></div></div>");
$templateCache.put("style/widgets/stroke-editor.html","<div ng-form=stroke class=style-editor-item><div class=title>Stroke</div><div class=controls><div data-dropdown><button type=button class=dropdown-toggle>{{model.strokeStyle}} <span class=caret></span></button><ul class=dropdown-menu role=menu><li ng-repeat=\"style in styleChoices.strokeStyle\" ng-click=\"model.strokeStyle=style\">{{style}}</li></ul></div><number-editor st-model=model property=strokeWidth max=64></number-editor><color-editor st-model=model property=strokeColor></color-editor><number-editor st-model=model property=strokeOpacity max=100></number-editor></div></div>");
$templateCache.put("style/widgets/symbol-editor.html","<div ng-form=symbol class=style-editor-item><div class=title>Symbol</div><div class=controls><graphic-editor ng-if=showGraphic symbol=model></graphic-editor><number-editor ng-if=showGraphic st-model=model property=size max=64></number-editor><color-editor ng-if=!hideColor st-model=model property=fillColor></color-editor><number-editor st-model=model property=fillOpacity max=100></number-editor><attribute-combo layer=layer include=double ng-if=showRotation st-model=model property=rotationAttribute></attribute-combo><div dropdown ng-if=showRotation><button type=button class=dropdown-toggle>{{model.rotationUnits}} <span class=caret></span></button><ul class=dropdown-menu role=menu><li ng-repeat=\"rotationUnit in styleChoices.rotationUnits\" ng-click=\"model.rotationUnits=rotationUnit\">{{rotationUnit}}</li></ul></div></div></div>");}]);