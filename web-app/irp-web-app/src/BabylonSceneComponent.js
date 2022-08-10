import { Engine, Scene } from '@babylonjs/core'
import React, { useEffect, useRef } from 'react'

let babylonCanvasStyle = {
	'width':'100%',
	'height':'100%',
	'display':'block',
	'WebkitTouchCallout': 'none',
	'WebkitUserSelect': 'none',
	'KhtmlUserSelect': 'none',
	'MozUserSelect': 'none',
	'msUserSelect': 'none',
	'userSelect': 'none',
	'outline': 'none',
	'WebkitTapHighlightColor': 'rgba(255, 255, 255, 0)' /* mobile webkit */
}

let babylonCanvasHiddenStyle = {
    'visibility': 'hidden',
	'width':'100%',
	'height':'100%',
	'display':'none',
	'WebkitTouchCallout': 'none',
	'WebkitUserSelect': 'none',
	'KhtmlUserSelect': 'none',
	'MozUserSelect': 'none',
	'msUserSelect': 'none',
	'userSelect': 'none',
	'outline': 'none',
	'WebkitTapHighlightColor': 'rgba(255, 255, 255, 0)' /* mobile webkit */
}

export default (props) => {
    const reactCanvas = useRef(null);
    const { antialias, engineOptions, adaptToDeviceRatio, sceneOptions, onRender, onSceneReady, ...rest } = props;
    useEffect(() => {
        if (reactCanvas.current) {
            const engine = new Engine(reactCanvas.current, antialias, engineOptions, adaptToDeviceRatio);
            const scene = new Scene(engine, sceneOptions);
            if (scene.isReady()) {
                props.onSceneReady(scene)
            } else {
                scene.onReadyObservable.addOnce(scene => props.onSceneReady(scene));
            }
            engine.runRenderLoop(() => {
                if (typeof onRender === 'function') {
                    onRender(scene);
                }
                //scene.render();
            })
            const resize = () => {
                scene.getEngine().resize();
            }
            if (window) {
                window.addEventListener('resize', resize);
            }
            return () => {
                scene.getEngine().dispose();
                if (window) {
                    window.removeEventListener('resize', resize);
                }
            }
        }
    }, [reactCanvas])
    return (
        <canvas style={props.hidden ? babylonCanvasHiddenStyle : babylonCanvasStyle} ref={reactCanvas} {...rest} />
    );
}