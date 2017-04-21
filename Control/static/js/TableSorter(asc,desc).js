    function TableSorter(table_id, dir) {
        var table = document.getElementById(table_id);
        table.onclick = function (event) {
            if (event.target.tagName !== 'TH') return;
            sortTable(event.target.cellIndex, event.target.getAttribute('data-type'));

            function sortTable(colNum, type) {
                if (type === null) {
                    return;
                }
                var tbody = table.getElementsByTagName('tbody')[0];
                var rowsArray = [].slice.call(tbody.rows);
                var compare;
                switch (type) {
                    case 'number':
                        compare = function (rowA, rowB) {
                            return rowA.cells[colNum].innerText - rowB.cells[colNum].innerText;
                        };
                        break;
                    case 'string':
                        compare = function (rowA, rowB) {
                            return rowA.cells[colNum].innerText.localeCompare(rowB.cells[colNum].innerText);
                        };
                        break;
                }
                rowsArray.sort(compare);
                if (dir === 'desc') {
                    rowsArray.reverse();
                    dir = 'asc';
                } else {
                    dir = 'desc';
                }
                table.removeChild(tbody);

                for (var i = 0; i < rowsArray.length; i++) {
                    tbody.appendChild(rowsArray[i]);
                }
                table.appendChild(tbody);


            }
        }
    }
