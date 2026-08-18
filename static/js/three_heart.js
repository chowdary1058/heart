// Glowing 3D Heart using Three.js for HeartCare.ai Hero Section

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('three-heart-container');
    if (!container) return;

    // Dimensions
    let width = container.clientWidth;
    let height = container.clientHeight || 400;

    // Scene
    const scene = new THREE.Scene();

    // Camera
    const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000);
    camera.position.z = 30;

    // Renderer
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Group to hold the heart and enable cursor interaction
    const mainGroup = new THREE.Group();
    scene.add(mainGroup);

    // Heart Shape
    const heartShape = new THREE.Shape();
    heartShape.moveTo(0, -4);
    // Draw heart curve programmatically
    heartShape.bezierCurveTo(0, -4, -1, 1, -5, 1);
    heartShape.bezierCurveTo(-9, 1, -9, 6, -9, 6);
    heartShape.bezierCurveTo(-9, 10, -5, 13.5, 0, 18);
    heartShape.bezierCurveTo(5, 13.5, 9, 10, 9, 6);
    heartShape.bezierCurveTo(9, 6, 9, 1, 5, 1);
    heartShape.bezierCurveTo(1, 1, 0, -4, 0, -4);

    // Extrude Settings
    const extrudeSettings = {
        depth: 3,
        bevelEnabled: true,
        bevelSegments: 5,
        steps: 2,
        bevelSize: 1.5,
        bevelThickness: 1.5
    };

    // Geometries
    const geometry = new THREE.ExtrudeGeometry(heartShape, extrudeSettings);
    geometry.center();
    geometry.rotateZ(Math.PI); // Rotate right side up

    // Materials - Outer Glass Shell & Inner Glowing Wireframe
    let isDark = document.documentElement.classList.contains('dark');
    
    function getColors(dark) {
        return {
            solid: dark ? 0xe11d48 : 0x0d9488,  // Rose vs Teal
            wireframe: dark ? 0xf43f5e : 0x14b8a6,
            lightIntensity: dark ? 2.5 : 1.8
        };
    }

    let colors = getColors(isDark);

    // Outer Mesh
    const material = new THREE.MeshPhongMaterial({
        color: colors.solid,
        emissive: colors.solid,
        emissiveIntensity: 0.15,
        shininess: 90,
        transparent: true,
        opacity: 0.3,
        flatShading: true
    });
    const heartMesh = new THREE.Mesh(geometry, material);
    mainGroup.add(heartMesh);

    // Inner Wireframe
    const wireframeMat = new THREE.MeshBasicMaterial({
        color: colors.wireframe,
        wireframe: true,
        transparent: true,
        opacity: 0.6
    });
    const wireframeMesh = new THREE.Mesh(geometry, wireframeMat);
    wireframeMesh.scale.set(0.98, 0.98, 0.98);
    mainGroup.add(wireframeMesh);

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);

    const dirLight1 = new THREE.DirectionalLight(0xffffff, colors.lightIntensity);
    dirLight1.position.set(10, 20, 15);
    scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0x14b8a6, 1.5);
    dirLight2.position.set(-10, -20, -10);
    scene.add(dirLight2);

    // Mouse movement interaction
    let mouseX = 0, mouseY = 0;
    let targetX = 0, targetY = 0;

    window.addEventListener('mousemove', (event) => {
        // Normalize mouse coordinates (-1 to 1)
        mouseX = (event.clientX / window.innerWidth) * 2 - 1;
        mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
    });

    // Theme Change Handler
    window.addEventListener('theme-changed', (e) => {
        const themeColors = getColors(e.detail.theme === 'dark');
        material.color.setHex(themeColors.solid);
        material.emissive.setHex(themeColors.solid);
        dirLight1.intensity = themeColors.lightIntensity;
        wireframeMat.color.setHex(themeColors.wireframe);
    });

    // Animation Loop
    const clock = new THREE.Clock();

    function animate() {
        requestAnimationFrame(animate);

        const elapsedTime = clock.getElapsedTime();

        // Standard rotation
        mainGroup.rotation.y = elapsedTime * 0.4;
        
        // Heartbeat pulse effect
        const pulse = 1.0 + Math.sin(elapsedTime * 4.0) * 0.04;
        mainGroup.scale.set(pulse, pulse, pulse);

        // Smooth cursor tracking
        targetX = mouseX * 0.3;
        targetY = mouseY * 0.3;

        mainGroup.rotation.x += (targetY - mainGroup.rotation.x) * 0.1;
        mainGroup.rotation.z += (targetX - mainGroup.rotation.z) * 0.1;

        renderer.render(scene, camera);
    }

    animate();

    // Window Resize Handler
    window.addEventListener('resize', () => {
        width = container.clientWidth;
        height = container.clientHeight || 400;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    });
});
