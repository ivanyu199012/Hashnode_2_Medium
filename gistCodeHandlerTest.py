#
import json
import ntpath
import  unittest

from gistCodeHandler import GistCodeHandler

class GistCodeUploaderTest( unittest.TestCase ) :

	def setUp(self):
		print ( f"Method: { self._testMethodName }" )
		self.file_path = "temp/Django_background_task.md"


	def test_0_read_file( self ):
		content = GistCodeHandler.read_file( self.file_path )
		self.assertEqual( "Introduction" in content, True )

	def test_1_convert_code_block_to_id( self ):
		content = GistCodeHandler.read_file( self.file_path )
		file_basename = ntpath.basename( self.file_path )
		id_2_code_block_info_dict, temp_markdown_text = GistCodeHandler.convert_code_block_to_id( file_basename, content )

		for id in id_2_code_block_info_dict:
			self.assertEqual( file_basename in id, True )
			code_block_info_dict = id_2_code_block_info_dict[ id ]
			self.assertEqual( code_block_info_dict[ GistCodeHandler.LANG_KEY ], "python" )
			self.assertEqual( id in temp_markdown_text, True )

		with open( "temp\id_2_code_block_info_dict.json", "w" ) as f:
			json.dump( id_2_code_block_info_dict, f, indent=4)

	def test_2_save_temp_markdown_file( self ):
		content = GistCodeHandler.read_file( self.file_path )
		file_basename = ntpath.basename( self.file_path )
		_, temp_markdown_text = GistCodeHandler.convert_code_block_to_id( file_basename, content )

		path = GistCodeHandler.save_file( file_basename, temp_markdown_text )
		self.assertEqual( path, f"temp/temp_{file_basename}" )

	def test_3_upload_code_block_to_gist( self ):
		id_2_code_block_info_dict = None
		with open("temp/id_2_code_block_info_dict.json", 'r', encoding='utf-8') as f:
			id_2_code_block_info_dict = json.load( f )

		id_2_gist_link_dict = GistCodeHandler.upload_code_block_to_gist( id_2_code_block_info_dict )
		print(f'{ id_2_gist_link_dict= }')
		for id in id_2_code_block_info_dict.keys():
			self.assertEqual( id in id_2_gist_link_dict, True )
			self.assertEqual( "https://gist.github.com/" in id_2_gist_link_dict[ id ], True )

		with open("temp/id_2_gist_link_dict.json", 'w', encoding='utf-8') as f:
			json.dump( id_2_gist_link_dict, f, indent=4)

	def test_4_delete_gists( self ):
		id_2_gist_link_dict : dict = None
		with open("temp/id_2_gist_link_dict.json", 'r', encoding='utf-8') as f:
			id_2_gist_link_dict = json.load( f )

		gist_id_list = [ gist_link.replace( "https://gist.github.com/", "" ) for gist_link in id_2_gist_link_dict.values() ]

		GistCodeHandler.delete_gists( gist_id_list )




if __name__ == '__main__':
	unittest.TestLoader.sortTestMethodsUsing = None
	unittest.main()