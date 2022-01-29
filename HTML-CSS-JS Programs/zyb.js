function click_speed_control() {
    document.querySelectorAll('.speed-control input').forEach(e=> {e.click()})
}

function click_start_button() {
    document.querySelectorAll('.animation-controls button').forEach(e=> {e.click()})
}

function click_play_button() {
    document.querySelectorAll('.play-button').forEach(e=> {e.click()})
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms)); }

async function cheat() {
    click_speed_control()
    click_start_button()
    for (let i=0; i < 5; i++) {
        click_play_button()
        await sleep(5000)
    }
}
