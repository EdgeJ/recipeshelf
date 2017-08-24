require 'test_helper'

class RecipeshelfControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get recipeshelf_index_url
    assert_response :success
  end

end
