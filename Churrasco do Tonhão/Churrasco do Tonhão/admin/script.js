const apiBaseUrl = "http://127.0.0.1:5000";

// Função para buscar reservas
document.getElementById("fetch-reservas-btn").addEventListener("click", async () => {
    const tableBody = document.querySelector("#reservas-table tbody");
    tableBody.innerHTML = ""; // Limpa a tabela antes de carregar
    try {
        const response = await fetch(`${apiBaseUrl}/reservas`);
        const reservas = await response.json();
        if (response.ok) {
            reservas.forEach(reserva => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${reserva.id}</td>
                    <td>${reserva.nome}</td>
                    <td>${reserva.telefone}</td>
                    <td>${reserva.lugares}</td>
                    <td>${reserva.data}</td>
                    <td>${reserva.horario}</td>
                    <td>
                        <select class="status-select" data-id="${reserva.id}">
                            <option value="Confirmada" ${reserva.status === 'Confirmada' ? 'selected' : ''}>Confirmada</option>
                            <option value="Pendente" ${reserva.status === 'Pendente' ? 'selected' : ''}>Pendente</option>
                        </select>
                    </td>
                    <td>
                        <button class="delete-btn" data-id="${reserva.id}">Excluir</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            // Adicionar o evento para excluir reserva
            document.querySelectorAll(".delete-btn").forEach(button => {
                button.addEventListener("click", async (e) => {
                    const reservaId = e.target.getAttribute("data-id");
                    const confirmDelete = confirm(`Tem certeza que deseja excluir a reserva com ID ${reservaId}?`);

                    if (confirmDelete) {
                        try {
                            const response = await fetch(`${apiBaseUrl}/excluir_reserva?id=${reservaId}`, { method: "DELETE" });
                            const result = await response.json();
                            if (response.ok) {
                                alert("Reserva excluída com sucesso!");
                                e.target.closest("tr").remove();  // Remove a linha da tabela
                            } else {
                                alert("Erro: " + result.error);
                            }
                        } catch (error) {
                            console.error("Erro ao excluir reserva:", error);
                        }
                    }
                });
            });

            // Atualizar o status da reserva quando o status for alterado
            document.querySelectorAll(".status-select").forEach(select => {
                select.addEventListener("change", async (e) => {
                    const reservaId = e.target.getAttribute("data-id");
                    const novoStatus = e.target.value;

                    try {
                        const response = await fetch(`${apiBaseUrl}/atualizar_reserva?id=${reservaId}&status=${novoStatus}`);
                        const result = await response.json();
                        if (response.ok) {
                            alert("Status da reserva atualizado com sucesso!");
                        } else {
                            alert("Erro: " + result.error);
                        }
                    } catch (error) {
                        console.error("Erro ao atualizar status:", error);
                    }
                });
            });
        } else {
            alert("Erro ao buscar reservas: " + reservas.error);
        }
    } catch (error) {
        console.error("Erro ao buscar reservas:", error);
    }
});
