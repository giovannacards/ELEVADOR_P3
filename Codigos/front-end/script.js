let msg = document.querySelector('div#msg');
let pos_atual = '';
let urlWebServer = "http://192.168.4.1";
let botaoMoverSelecionado = false; 
let botaoSelecionado = null; 


function selecionarPosicao(btn) {
  msg.innerHTML = 'Posição selecionada';

  let btn_value = btn.value;
  pos_atual = btn_value;

  if (!botaoMoverSelecionado) {
    if (btn_value === botaoSelecionado) {
        btn.classList.remove('botao-selecionado');
        botaoSelecionado = null;
    } else {
        if (botaoSelecionado) {
            botaoSelecionado.classList.remove('botao-selecionado');
        }
        btn.classList.add('botao-selecionado');
        botaoSelecionado = btn;
    }
    verificarBotaoMover();
  }
}

function resetarPosicao() {
  msg.innerHTML = 'Posição resetada, escolha outra';

  const botoesPosicao = document.querySelectorAll('.botao-posição');
  for (const botao of botoesPosicao) {
    botao.classList.remove('botao-selecionado');
  }

  botaoSelecionado = null;
  verificarBotaoMover();
}


function moverElevador() {
  msg.innerHTML = 'Movendo...';

  if (!botaoMoverSelecionado) {
    botaoMoverSelecionado = true;
    document.getElementById("mover").classList.add('botao-selecionado'); 
    desabilitarBotoesPosicao(); 
    setTimeout(function () {
        botaoMoverSelecionado = false;
        document.getElementById("mover").classList.remove('botao-selecionado'); 
        ativarBotoesPosicao();
    }, 80000); 
}
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

let isPressed = false
var btnDispensar = document.querySelector("#dispensar");
btnDispensar.addEventListener("click", function(){
    isPressed = true;
    console.log(`Pressionado = ${isPressed}`);
    dispensar();
});

function dispensar() {
  msg.innerHTML = 'Dispensando...';
    fetch(`${urlWebServer}/dispensar`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ isPressionado: isPressed }),
    })
    .catch(error => {
        console.error('Erro na solicitação:', error);
    });
    isPressed = false

    if (!botaoMoverSelecionado) {
      botaoMoverSelecionado = true;
      document.getElementById("dispensar").classList.add('botao-selecionado'); 
      desabilitarBotoesPosicao(); 
      setTimeout(function () {
          botaoMoverSelecionado = false;
          document.getElementById("dispensar").classList.remove('botao-selecionado'); 
          ativarBotoesPosicao();
      }, 30000);
}
}

function desabilitarBotoesPosicao() {
  const botoesPosicao = document.querySelectorAll('.botao-posição');
  for (const btn_value of botoesPosicao) {
    btn_value.disabled = true; 
  }
}


function ativarBotoesPosicao() {
  const botoesPosicao = document.querySelectorAll('.botao-posição');
  for (const btn_value of botoesPosicao) {
    btn_value.disabled = false; 
    msg.innerHTML = 'Selecione uma posição';
  }
}

function verificarBotaoMover() {
    const botaoMover = document.getElementById("mover");

    if (botaoMoverSelecionado || botaoSelecionado) {
        botaoMover.disabled = false;
    } else {
        botaoMover.disabled = true;
    }
}
