document.addEventListener("DOMContentLoaded", function () {
    const dataInicioInput = document.getElementById("id_data_inicio");
    const horarioInicioInput = document.getElementById("id_horario_inicio");
    const horarioFimInput = document.getElementById("id_horario_fim");
    const colaboradoresSelect = document.getElementById("id_colaboradores");

    function atualizarColaboradores() {
        const data_inicio = dataInicioInput.value;
        const horario_inicio = horarioInicioInput.value;
        const horario_fim = horarioFimInput.value;

        if (data_inicio && horario_inicio && horario_fim) {
            fetch(`/colaboradores-disponiveis/?data_inicio=${data_inicio}&horario_inicio=${horario_inicio}&horario_fim=${horario_fim}`)
                .then(response => response.json())
                .then(data => {
                    colaboradoresSelect.innerHTML = "";
                    
                    if (data.colaboradores.length === 0) {
                        const option = document.createElement("option");
                        option.text = "Nenhum colaborador disponível";
                        option.disabled = true;
                        colaboradoresSelect.appendChild(option);
                    } else {
                        data.colaboradores.forEach(colaborador => {
                            const option = document.createElement("option");
                            option.value = colaborador.id;
                            option.text = colaborador.nome;
                            colaboradoresSelect.appendChild(option);
                        });
                    }
                });
        }
    }

    dataInicioInput.addEventListener("change", atualizarColaboradores);
    horarioInicioInput.addEventListener("change", atualizarColaboradores);
    horarioFimInput.addEventListener("change", atualizarColaboradores);
});