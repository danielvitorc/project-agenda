function abrirModalDetalhes(botao) {
    document.getElementById('modalLocal').textContent = botao.dataset.local;
    document.getElementById('modalData').textContent = botao.dataset.data;
    document.getElementById('modalHorario').textContent = botao.dataset.horario;
    document.getElementById('modalDescricao').textContent = botao.dataset.descricao;
    document.getElementById('modalColaboradores').textContent = botao.dataset.colaboradores;

    var modal = new bootstrap.Modal(document.getElementById('modalReuniao'));
    modal.show();
}