import { SERVER_ADRESS } from './const'

export const login = async (username, password) => {
    return await fetch(`${SERVER_ADRESS}/get-token`, {
        method: 'POST',
        body: JSON.stringify({ username: username, password: password }),
        headers: { 'Content-Type': 'application/json' },
    }).then((res) => res.json())
}
