import { SceneLoader, Vector3, Color3, DynamicTexture, 
    Mesh, AbstractMesh, StandardMaterial, 
    TransformNode, MeshBuilder} from "@babylonjs/core";

import "@babylonjs/loaders/glTF";

export default class Character{

    constructor(app){
        this.app = app;
        // The first parameter can be used to specify which mesh to import. Here we import all meshes
        SceneLoader.ImportMesh("", "assets/", "character.glb", this.app.scene, (characterMeshes) => {
            this.characterModel = characterMeshes;
        });
        this.app.scene.activeCamera.alpha += Math.PI;
    }

}