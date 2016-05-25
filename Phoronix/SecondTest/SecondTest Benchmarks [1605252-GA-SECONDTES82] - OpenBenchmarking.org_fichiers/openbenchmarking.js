
//
// OpenBenchmarking.org results comparison functions
//

var result_comparison_r = new Array();

function oborg_page_loaded()
{
	//document.getElementById('oborg_horizontal_top_nav_search').style.visibility = 'visible';
}
function oborg_user_search()
{
	if(document.getElementById('user_search').value.length < 3)
	{
		//alert('Enter a longer search query.');
		//return false;
	}

	oborg_search(document.getElementById('user_search').value);
}
function oborg_search_quick_compare(form)
{
	var compare_url = '/result/' + document.search_quick_compare_form.quick_compare_base.value;

	for(var i = 0; i < document.search_quick_compare_form.quick_compare_ids.length; i++)
	{
		if(document.search_quick_compare_form.quick_compare_ids[i].checked)
			compare_url += "," + document.search_quick_compare_form.quick_compare_ids[i].value;
	}

	document.location = compare_url + "&compare";
}
function oborg_add_result_id_to_session_compare_storage(public_id)
{
	if(typeof(Storage) !== 'undefined')
	{
		if(sessionStorage.session_compare_ids)
		{
			var ids = JSON.parse(sessionStorage.session_compare_ids);

		}
		else
		{
			var ids = [];
		}

		if(ids.indexOf(public_id) == -1)
		{
			ids.push(public_id);
		}

		sessionStorage.session_compare_ids = JSON.stringify(ids);
	}
}
function oborg_add_result_id_to_local_compare_storage(public_id)
{
	if(typeof(Storage) !== 'undefined')
	{
		if(localStorage.local_viewed_ids)
		{
			var ids = JSON.parse(localStorage.local_viewed_ids);

			if(ids.length > 20)
			{
				for(var i = 0; i < (ids.length - 20); i++)
				{
					ids.shift();
				}
			}
		}
		else
		{
			var ids = [];
		}

		if(ids.indexOf(public_id) == -1)
		{
			ids.push(public_id);
		}

		localStorage.local_viewed_ids = JSON.stringify(ids);
	}
}
function oborg_get_cookie(name)
{
	var x, cookies = document.cookie.split(';');

	for(var i = 0; i < cookies.length; i++)
	{
		x = cookies[i].substr(0, cookies[i].indexOf('='));
		x = x.replace(/^\s+|\s+$/g, '');

		if(x == name)
		{
			return unescape(cookies[i].substr(cookies[i].indexOf('=') + 1));
		}
	}
}
function oborg_list_comparison(div_id, public_id)
{
	if(result_comparison_r.indexOf(public_id) != -1)
	{
		oborg_list_to_comparison('');
	}
	else
	{
		document.getElementById(div_id).style.border = '1px solid #E12128';
		document.getElementById(div_id + '_compare').innerHTML = 'Compare Results';
		result_comparison_r.push(public_id);
	}
	oborg_add_result_id_to_session_compare_storage(public_id);

	return false;
}
function oborg_rpage_compare(click_tag, public_id, compare_button)
{
	if(public_id == 'compare')
	{
		oborg_list_to_comparison('&compare');
	}
	else
	{
		if(result_comparison_r.indexOf(public_id) != -1)
		{
			click_tag.style.fontWeight = 'normal';
			result_comparison_r.splice(result_comparison_r.indexOf(public_id), 1);
		}
		else
		{
			click_tag.style.fontWeight = 'bold';
			result_comparison_r.push(public_id);
		}

		if(result_comparison_r.length > 1)
		{
			document.getElementById(compare_button).style.display = 'block';
		}
		else
		{
			document.getElementById(compare_button).style.display = 'none';
		}
	}

	return false;
}
function oborg_search(s)
{
	document.location = '/s/' + s;
}
function oborg_test_page(i)
{
	document.location = '/test/' + i;
}
function oborg_list_to_comparison(postfix)
{
	document.location = '/result/' + result_comparison_r.toString() + postfix;
}
function oborg_switch_display_tab(display_tab, switch_to)
{
	var aNodes = document.getElementById(display_tab + '_attachment').childNodes;
	var dNodes = document.getElementById(display_tab + '_blockquote').childNodes;

	for(var i = 0; i < aNodes.length; i++)
	{
		aNodes[i].getElementsByTagName('div')[0].style.background = '#E12128';
	}
	for(var i = 0; i < dNodes.length; i++)
	{
		if(dNodes[i].style.display == 'block')
		{
			dNodes[i].style.display = 'none';
		}
	}

	document.getElementById('display_tab_' + switch_to + '_header').style.background = '#1B75BB';
	document.getElementById('display_tab_' + switch_to).style.display = 'block';

	if(document.getElementById('display_tab_' + switch_to).getElementsByTagName('input').length > 0)
	{
		document.getElementById(display_tab + '_submit').style.display = 'block';
	}
	else
	{
		document.getElementById(display_tab + '_submit').style.display = 'none';
	}
}
function oborg_finder_set_type(category, finder_form)
{
	document.getElementById('oborg_finder_options').style.display = 'block';

	if(category == 'GPU')
	{
		document.getElementById('oborg_finder_options_graphics').style.display = 'block';
	}
	else
	{
		document.getElementById('oborg_finder_options_graphics').style.display = 'none';
	}
}
function ob_checkbox_toggle_result_comparison(pprid)
{
	if(typeof(Storage) !== 'undefined')
	{
		if(localStorage.comparison_ob_public_ids)
		{
			var ids = JSON.parse(localStorage.comparison_ob_public_ids);
		}
		else
		{
			var ids = [];
		}

		if(pprid != '')
		{
			if(ids.indexOf(pprid) == -1)
			{
				// Add the PPRID to comparison
				ids.push(pprid);
			}
			else
			{
				ids.splice(ids.indexOf(pprid), 1);
				if(document.getElementById("result_select_" + pprid))
				{
					document.getElementById("result_select_" + pprid).style.background = "#f1f1f1";
				}
				document.getElementById("result_compare_checkbox_" + pprid).checked = false;
			}

			localStorage.comparison_ob_public_ids = JSON.stringify(ids);
		}

		if(ids.length > 0)
		{
			for(var i = 0; i < ids.length; i++)
			{
				if(document.getElementById("result_select_" + ids[i]))
				{
					document.getElementById("result_select_" + ids[i]).style.background = "#ABB3B3";
				}
				if(ids.length > 1 && document.getElementById("result_run_compare_link_" + ids[i]))
				{
					document.getElementById("result_run_compare_link_" + ids[i]).innerHTML = 'Compare Results (' + ids.length + ')';
					document.getElementById("result_run_compare_link_" + ids[i]).style.visibility = 'visible';
				}
				if(document.getElementById("result_compare_checkbox_" + ids[i]))
				{
					document.getElementById("result_compare_checkbox_" + ids[i]).checked = true;
				}
			}

			document.getElementById("ob_result_compare_info_box").innerHTML = "Compare " + ids.length + " Selected Results";
			document.getElementById("ob_result_compare_info_box").style.display = 'inline';
		}
		else
		{
			if(document.getElementById("ob_result_compare_info_box"))
			{
				document.getElementById("ob_result_compare_info_box").style.display = 'none';
			}
		}
	}

	return false;
}
function ob_clear_comparison_storage()
{
	if(localStorage.comparison_ob_public_ids)
	{
		var ids = JSON.parse(localStorage.comparison_ob_public_ids);

		if(ids.length > 0)
		{
			for(var i = 0; i < ids.length; i++)
			{
				if(document.getElementById("result_compare_checkbox_" + ids[i]))
				{
					document.getElementById("result_compare_checkbox_" + ids[i]).checked = false;
				}
				if(document.getElementById("result_select_" + ids[i]))
				{
					document.getElementById("result_select_" + ids[i]).style.background = "#f7fbff";
				}
			}
		}
		localStorage.removeItem("comparison_ob_public_ids");
	}
	document.getElementById("ob_result_compare_info_box").style.display = 'none';
}
function ob_generate_comparison(ext)
{
	if(typeof(Storage) !== 'undefined' && localStorage.comparison_ob_public_ids)
	{
		var ids = JSON.parse(localStorage.comparison_ob_public_ids);
		localStorage.removeItem("comparison_ob_public_ids");
		window.location.href = ext + ids.join(',');
	}
}
function ob_add_to_this_comparison()
{
	var checkboxes = document.getElementsByName('form_add_to_result_comparison');
	var new_url = document.URL;
	for(var i = 0; i < checkboxes.length; i++)
	{
		if(checkboxes[i].checked)
		{
			new_url += ',' + checkboxes[i].value;
		}
	}
	window.location = new_url;
}
