def html_str(table_data):
    html_ = '''
      <html>
      <body>
      <p><em>Alert generation logic:</em></p>
<ul>
    <li>Alerts will be at every defined interval</li>
    <li>All cameras that are offline, their names will be included. This could be due to various reasons. For this
        first check:
        <ul>
            <li>If cameras are streamig in the VLC (of the PC where software is installed)</li>
            <li>PC internet is working by taking remote Anydesk from any other PC or mobile phone</li>
            <li>If Darsa software is open - if not then restart it</li>
            <li>If all of the above are fine, contact Darsa team</li>
        </ul>
    </li>
    <li>In subsequent alerts, if cameras are still offline, you will be able to see offline aging.</li>
</ul>
      
<table style="border: 1px solid orange; border-collapse: collapse">
  <tr>
    <th style="border: 1px solid orange">Camera</th>
    <th style="border: 1px solid orange">Facility</th>
  </tr>

{0}
</table>
</body>
</html>
'''.format(table_data)
    return html_