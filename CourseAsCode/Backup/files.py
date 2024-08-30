import time
import xml.etree.ElementTree as ET


# todo: move to file service
def create_xml(backup_dir, sections):
    # Create a new XML tree
    files = ET.Element("files")

    for sec in sections:
        for f in sec.files:
            file_tag = ET.SubElement(files, "file")
            file_tag.set('id', str(f.module_id))

            hash_tag = ET.SubElement(file_tag, "contenthash")
            hash_tag.text = str(f.content_hash)
            hash_tag.tail = '\n'

            context = ET.SubElement(file_tag, "contextid")
            context.text = str(f.context_id)
            context.tail = '\n'

            component = ET.SubElement(file_tag, "component")
            component.text = f.component
            component.tail = '\n'

            file_area = ET.SubElement(file_tag, "filearea")
            file_area.text = f.area
            file_area.tail = '\n'

            item_id = ET.SubElement(file_tag, "itemid")
            item_id.text = str(0)   # it is not the file id, surprisingly
            item_id.tail = '\n'

            file_path = ET.SubElement(file_tag, "filepath")
            file_path.text = f.path
            file_path.tail = '\n'

            file_name = ET.SubElement(file_tag, "filename")
            file_name.text = f.name
            file_name.tail = '\n'

            user_id = ET.SubElement(file_tag, "userid")
            user_id.text = str(f.user_id)
            user_id.tail = '\n'

            size = ET.SubElement(file_tag, "filesize")
            size.text = str(f.size)
            size.tail = '\n'

            mimetype = ET.SubElement(file_tag, "mimetype")
            mimetype.text = "application/" + f.type
            mimetype.tail = '\n'

            status = ET.SubElement(file_tag, "status")
            status.text = "0"
            status.tail = '\n'

            created = ET.SubElement(file_tag, "timecreated")
            created.text = str(int(time.time()))
            created.tail = '\n'

            modified = ET.SubElement(file_tag, "timemodified")
            modified.text = str(int(time.time()))
            modified.tail = '\n'

            source = ET.SubElement(file_tag, "source")
            source.text = f.name
            source.tail = '\n'
            author = ET.SubElement(file_tag, "author")
            author.text = "$@NULL@$"
            author.tail = '\n'
            license = ET.SubElement(file_tag, "license")
            license.text = "$@NULL@$"
            license.tail = '\n'
            sortorder = ET.SubElement(file_tag, "sortorder")
            sortorder.text = "0"
            sortorder.tail = '\n'# todo
            repository_type = ET.SubElement(file_tag, "repositorytype")
            repository_type.text = "$@NULL@$"
            repository_type.tail = '\n'
            repository_id = ET.SubElement(file_tag, "repositoryid")
            repository_id.text = "$@NULL@$"
            repository_id.tail = '\n'
            reference = ET.SubElement(file_tag, "reference")
            reference.text = "$@NULL@$"
            reference.tail = '\n'

    tree = ET.ElementTree(files)
    tree.write(backup_dir + "/files.xml", encoding='utf-8', xml_declaration=True)

