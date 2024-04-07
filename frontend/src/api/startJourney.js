import { SERVER_ADRESS } from './const'

export const startJourney = async (duration, boatType) => {
    const data = new Date()
    const body = JSON.stringify({
        duration: duration,
        start_date: new Date(),
        ship_id: boatType,
    })

    return await fetch(`${SERVER_ADRESS}/journeys/`, {
        method: 'POST',
        body: body,
        headers: {
            'Content-Type': 'application/json',
        },
    }).then((res) => res.json())
}
