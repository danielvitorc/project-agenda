document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var statusFilter = document.getElementById('statusFilter');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'pt-br',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        slotMinTime: "07:00:00",
        slotMaxTime: "20:00:00",
        events: function(fetchInfo, successCallback, failureCallback) {
            fetch('/eventos_json/') // Chama a API de eventos
                .then(response => response.json())
                .then(data => {
                    let selectedStatus = statusFilter ? statusFilter.value : "todos";
                    let eventos = data
                        .filter(evento => selectedStatus === "todos" || evento.status === selectedStatus) // Filtragem pelo status
                        .map(evento => ({
                            title: evento.title,
                            start: evento.start,
                            end: evento.end,
                            status: evento.status,
                            extendedProps: {
                                local: evento.local || "Não informado",
                                descricao: evento.descricao || "Sem descrição",
                                colaboradores: evento.colaboradores || "Nenhum"
                            },
                            backgroundColor: evento.status === "aprovado" ? "#007bff" : evento.status === "pendente" ? "#f39c12" : "#28a745",
                            borderColor: evento.status === "aprovado" ? "#007bff" : evento.status === "pendente" ? "#f39c12" : "#28a745"
                        }));
                    successCallback(eventos);
                })
                .catch(error => {
                    console.error("Erro ao buscar eventos:", error);
                    failureCallback(error);
                });
        },
        eventClick: function(info) {
            let evento = info.event;
            let props = evento.extendedProps || {};

            document.getElementById('modalReuniaoLabel').textContent = evento.title || "Sem título";
            document.getElementById('modalLocal').textContent = props.local || "Não informado";
            document.getElementById('modalData').textContent = evento.start 
                ? evento.start.toLocaleDateString('pt-BR') 
                : "Sem data";
            document.getElementById('modalHorario').textContent = evento.start && evento.end
                ?  evento.start.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }) + " - " + evento.end.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
                : "Sem horário";
            document.getElementById('modalDescricao').textContent = props.descricao || "Sem descrição";
                // Exibir colaboradores um abaixo do outro
            let modalColaboradores = document.getElementById('modalColaboradores');
            modalColaboradores.innerHTML = "";  // Limpar antes de adicionar novos itens

            if (props.colaboradores) {
                let listaColaboradores = document.createElement("ul"); // Criar uma lista
                props.colaboradores.split(", ").forEach(colab => {
                    let item = document.createElement("li");
                    item.textContent = colab;
                    listaColaboradores.appendChild(item);
                });
                modalColaboradores.appendChild(listaColaboradores);
            } else {
                modalColaboradores.textContent = "Nenhum";
            }

            var modal = new bootstrap.Modal(document.getElementById('modalReuniao'));
            modal.show();
        }
    });

    calendar.render();

    if (statusFilter) {
        statusFilter.addEventListener("change", function() {
            calendar.refetchEvents();
        });
    }
});