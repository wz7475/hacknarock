import * as THREE from 'three'
import React, { useEffect, useMemo, useState } from 'react'
import { Canvas, useFrame, useLoader, useThree } from '@react-three/fiber'
import { OrbitControls, OrthographicCamera } from '@react-three/drei'
import useMeasure from 'react-use-measure'
import { createNoise3D } from 'simplex-noise'
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader'

const noise = createNoise3D()
const swingNoise = createNoise3D()

const WaterChunk = (props) => {
    const [time, setTime] = useState(0)
    const geometry = useMemo(() => {
        return new THREE.PlaneGeometry(
            props.size,
            props.size,
            props.resolution,
            props.resolution
        )
    }, [])

    useFrame(({ clock }) => {
        setTime(clock.getElapsedTime() / 3)
    })

    useMemo(() => {
        const position = geometry.getAttribute('position')

        for (let i = 0; i < position.count; i++) {
            let x = position.getX(i)
            let y = position.getY(i)
            let z = position.getZ(i)

            z =
                noise(
                    (x + props.x * props.size) * props.scale,
                    (y + -props.y * props.size) * props.scale,
                    time
                ) * props.height

            position.setXYZ(i, x, y, z)
            position.needsUpdate = true
        }
    }, [time])

    return (
        <mesh
            geometry={geometry}
            rotation={[-Math.PI / 2, 0, 0]}
            position={[props.x * props.size, 0, props.y * props.size]}
            receiveShadow={true}
        >
            <meshStandardMaterial
                color={'steelblue'}
                flatShading={true}
            />
        </mesh>
    )
}

const Water = (props) => {
    const size = 8
    const resolution = 16
    const scale = 1
    const height = 0.1

    const gridSize = 5

    /*
    const state = useThree()

    useEffect(() => {
        const callback = (e) => {
            let x = (2 * e.offsetX) / e.target.width - 1
            let y = (2 * e.offsetY) / e.target.height - 1

            const raycaster = new THREE.Raycaster()
            raycaster.setFromCamera(new THREE.Vector2(x, y), state.camera)
            console.log(raycaster)
            console.log(
                x,
                y,
                raycaster.ray.intersectPlane(
                    new THREE.Plane(new THREE.Vector3(0, 1, 0)),
                    new THREE.Vector3(0, 0, 0)
                )
            )
        }
        document.addEventListener('mousedown', callback)

        return () => {
            document.removeEventListener('mousedown', callback)
        }
    })
    */

    const chunks = useMemo(() => {
        const result = []
        for (let x = -gridSize; x <= gridSize; x++) {
            for (let y = -gridSize; y <= gridSize; y++) {
                result.push([x, y])
            }
        }

        return result
    }, [])

    return (
        <>
            {chunks.map(([x, y]) => (
                <WaterChunk
                    x={x}
                    y={y}
                    size={size}
                    resolution={resolution}
                    scale={scale}
                    height={height * props.instability}
                />
            ))}
        </>
    )
}

const Camera = (props) => {
    const ratio = props.bounds.height / props.bounds.width
    const frustum = 800
    const horizonal = ratio < 1 ? frustum / ratio : frustum
    const vertical = ratio < 1 ? frustum : frustum * ratio
    return (
        <OrthographicCamera
            makeDefault
            zoom={80}
            top={vertical}
            bottom={-vertical}
            left={-horizonal}
            right={horizonal}
            near={0.1}
            far={2000}
            position={[100, 80, 100]}
            rotation={new THREE.Euler(-Math.PI / 6, Math.PI / 4, 0, 'YXZ')}
        />
    )
}

const Boat = (props) => {
    const geometry = useLoader(STLLoader, '/assets/low poly benchy.stl')
    const wakeTexture = useLoader(THREE.TextureLoader, '/assets/wake.png')

    const [swing, setSwing] = useState([0, 0])

    useFrame(({ clock }) => {
        setSwing([
            (props.instability *
                (Math.PI *
                    (swingNoise(
                        props.position[0],
                        props.position[1] + 3,
                        clock.getElapsedTime() / 3
                    ) -
                        0.5))) /
                50,
            (props.instability *
                (Math.PI *
                    (swingNoise(
                        props.position[0] + 3,
                        props.position[1],
                        clock.getElapsedTime() / 3
                    ) -
                        0.5))) /
                50,
        ])
    })

    const boatPosition = [props.position[0], -0.2, props.position[1]]

    return (
        <>
            <mesh
                geometry={geometry}
                scale={0.05}
                rotation={[-Math.PI / 2 + swing[0], swing[1], Math.PI / 2]}
                position={boatPosition}
                castShadow={true}
                receiveShadow={true}
            >
                <meshPhongMaterial
                    color={props.color}
                    flatShading={true}
                />
            </mesh>
        </>
    )
}

const BoatFleet = (props) => {
    const state = useThree()

    const boats = useMemo(() => {
        const result = []

        const visited = new Set([])
        const positions = [[0, 0]]
        for (let [type, count] of props.boats) {
            while (count > 0) {
                const pos = positions.shift()
                if (!visited.has(`${pos[0]},${pos[1]}`)) {
                    visited.add(`${pos[0]},${pos[1]}`)
                    positions.push([pos[0] - 1, pos[1]])
                    positions.push([pos[0] + 1, pos[1]])
                    positions.push([pos[0], pos[1] - 1])
                    positions.push([pos[0], pos[1] + 1])

                    if (Math.random() > 0.5 && (pos[0] !== 0 || pos[1] !== 0)) {
                        result.push({
                            type,
                            pos: [
                                4 * pos[0] + 2 * (Math.random() - 0.5),
                                5 * pos[1] + 2 * (Math.random() - 0.5),
                            ],
                        })
                        count -= 1
                    }
                }
            }
        }

        console.log(result)

        return result
    }, [props.boats])

    useEffect(() => {
        const screenPositions = boats.map(({ type, pos }) =>
            new THREE.Vector3(pos[0], 0, pos[1]).project(state.camera)
        )

        let maxX = -Infinity
        let maxY = -Infinity
        console.log(screenPositions)

        for (const pos of screenPositions) {
            maxX = Math.max(maxX, Math.abs(pos.x))
            maxY = Math.max(maxY, Math.abs(pos.y))
        }

        const zoomFactor = 0.8 / Math.max(maxX, maxY)
        console.log(maxX, maxY, zoomFactor)
        state.camera.zoom *= zoomFactor
        state.camera.updateProjectionMatrix()
    }, [boats, state.camera])

    return (
        <>
            {boats.map(({ type, pos }) => (
                <Boat
                    color="green"
                    instability={3}
                    position={pos}
                />
            ))}
        </>
    )
}

function ShipBackground() {
    const [ref, bounds] = useMeasure()

    return (
        <Canvas
            style={{
                height: '100vh',
            }}
            ref={ref}
            shadows={true}
        >
            <ambientLight intensity={Math.PI / 3} />
            <directionalLight
                intensity={1}
                position={[1, 0.5, 1]}
            />
            <directionalLight
                intensity={1}
                position={[-1, 2, 1]}
                castShadow={true}
            />

            <Water instability={3} />
            <Boat
                color="goldenrod"
                instability={3}
                position={[0, 0]}
            />

            <BoatFleet boats={[[5, 15]]} />

            <axesHelper args={[5]} />

            <Camera bounds={bounds} />
            <OrbitControls />
        </Canvas>
    )
}

export default ShipBackground
