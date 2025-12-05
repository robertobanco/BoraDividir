# IMPLEMENTAÇÃO CONSOLIDADA DOS 4 AJUSTES

## AJUSTE 1: Mostrar parcela atual (ex: 2/6)
- Localização: DomesticExpensesManager.tsx, linha 372
- Calcular: qual parcela está sendo exibida baseado na data inicial e mês atual
- Formato: "2/6" em vez de apenas "6x"

## AJUSTE 2: Corrigir "Divisão" → "Responsabilidade"
- Localização: Modal de adicionar/editar despesa
- Trocar label de "Divisão" para "Responsabilidade pelo pagamento"
- Clarificar que é quem DEVE pagar, não quem pagou

## AJUSTE 3: Mostrar responsabilidade no detalhamento
- Localização: Linha 351 do DomesticExpensesManager
- Formato atual: "Pago por Beto"
- Formato novo: "Pago por Beto (Beto 100%/0% Lise)"
- Aplicar também no compartilhamento WhatsApp

## AJUSTE 4: Exportação com opções
- Manter JSON para backup/importação
- Adicionar modal ao clicar em Exportar:
  - Opção 1: WhatsApp (já existe)
  - Opção 2: Excel (novo - apenas visualização)
- Excel: gerar planilha com despesas do mês atual, sem recorrências infinitas

Vou implementar um de cada vez para garantir qualidade.
