let msg = document.querySelector('div#msg');
let pos_atual = '';
let urlWebServer = "http://192.168.207.74";

function obterDadosElevador() {
  const elevatorDataElement = document.getElementById('elevator-data');
  fetch('/json/elevator_positions.json')
    .then(response => {
      if (!response.ok) {
        throw new Error('Erro na solicitação: ' + response.status);
      }
      return response.json();
    })
    .then(data => {
      console.log('Dados recebidos:', data);
      elevatorDataElement.innerHTML = `X: Posições: ${data.x}, Y: ${data.y}`;
    })
    .catch(error => {
      console.error('Erro na solicitação:', error);
    });
}

function selecionarPosicao(btn) {
  let btn_value = btn.value;
  pos_atual = btn_value;
}

function resetarPosicao() {
  msg.innerHTML = 'Posição resetada (origem)';
}

function moverElevador() {
  obterDadosElevador();
  if (pos_atual !== '') {
    fetch(`${urlWebServer}/moverElevador`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ position: pos_atual }),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Erro na solicitação: ' + response.status);
        }
        return response.json();
      })
      .then(data => {
        console.log('Resposta do ESP32:', data);
        msg.innerHTML = `Elevador movido para a posição ${pos_atual}`;
      })
      .catch(error => {
        console.error('Erro na solicitação:', error);
      });
  } else {
    msg.innerHTML = 'Selecione uma posição antes de mover o elevador';
  }
}

