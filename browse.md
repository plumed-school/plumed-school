Browse the lessons 
-----------------------------
The lessons that have been submitted to the PLUMED-TUTORIALS are listed below.  PLUMED-TUTORIAL monitors whether PLUMED input files in these lessons are compatible with the current and development 
versions of the code and integrates links from these files to the PLUMED manual.

{:#browse-table .display}
| ID | Name | Instructors | Description | Actions |
|:--------:|:--------:|:---------:|:---------:|:---------:|:---------:|:---------:|
{% for item in site.data.lessons %}| {{ item.id }} | [{{ item.title }}]({{ item.path }}) | {{ item.instructors | split: " " | last}} {{ item.instructors | split: " " | first | slice: 0}}. | {{ item.description }} | {{ item.actions }} |
{% endfor %}

<script>
$(document).ready(function() {
var table = $('#browse-table').DataTable({
  "dom": '<"search"f><"top"il>rt<"bottom"Bp><"clear">',
  language: { search: '', searchPlaceholder: "Search project..." },
  buttons: [
        'copy', 'excel', 'pdf'
  ],
  "columnDefs": [ 
     { "targets": 4, "visible": false }
  ],
  "order": [[ 0, "desc" ]]
  });
$('#browse-table-searchbar').keyup(function () {
  table.search( this.value ).draw();
  });
});
</script>
