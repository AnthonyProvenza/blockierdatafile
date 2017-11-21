import bdf

BDF = bdf.BDF2(True)

read = BDF.getDF("something.bdf")

writen = BDF.addNewRow(read, "all", "another row 1", "another row 2")

BDF.write("otherstuff.bdf", writen, compressed=True)

writen = BDF.deleteRow(writen, "all", -1)
