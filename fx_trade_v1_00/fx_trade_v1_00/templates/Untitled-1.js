var bookListName = ["Java", "Scala", "Swift", "Swift", "Swift", "HTML", "MySQL", "CSS", "JQuery", "GO", "Swift", "Swift"];
var bookListimage = ["http://dol.ismcdn.jp/mwimgs/f/2/670m/img_f2f389df9c8af1817b1ff8bc8e22b4921161403.jpg",
    "http://blog-imgs-30.fc2.com/k/o/b/kobeyakei/harborland090402-002.jpg",
    "http://www.ikuta-taxi.com/image/C8A1B4DBBBB3A1A1CCEBB7CA.jpg",
    "https://3.bp.blogspot.com/-mSKBrOngSjk/UtsicG_zc8I/AAAAAAAAGvw/QRb7P5AQLsk/s2560/night-view-wallpaper-8579590420_09d787d656_o.jpg",
    "http://websoku.jp/wp-content/uploads/2015/06/wpid-ReFAxJI.jpg",
    "https://photo1.ganref.jp/photo/0/e0c23b11e21ee6a8969431b17753983c/thumb5.jpg",
    "http://dreamearth.jp/php/wp-content/gallery/hoka14/SDIM7747.jpg",
    "http://www.bigwowo.com/wp-content/uploads/2011/03/Aomori_bay.jpg",
    "http://yakei.jp/photo/pc/selion2.jpg",
    "https://one-piece.com/assets/images/anime/character/data/chopper/img.jpg",
    "http://miteco.jp/wp/wp-content/uploads/2017/02/iwamotoyama_ee-1200x880.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSBukTUYAalnXmzsq93qVeGEeUrGARhfmq4PKoi0cTcd2XAO9ytA"
]
var bookList = [];


$(function () {
    $('button').click(function () {
        if (window.matchMedia('(min-width: 900px)').matches) {

            $('.imageTable').empty();
            var $search = $('#searchAns').val();

            var trCount = 4;

        } else {

            $('.imageTable').empty();
            var $search = $('#searchClass').val();

            var trCount = 2;
        }
        // var bookListName = ["Java", "Scala","JavaScript","Swift","C#","HTML","MySQL","CSS","JQuery","GO","Swift"];
        let searchAns = [];
        var result2 = 0;

        while (0 < bookListName.length) {
            if (result2 === 0) {
                var result2 = bookListName.indexOf($search, result2);
                searchAns.push(result2);
            } var result2 = bookListName.indexOf($search, result2 + 1); if (result2 === -1) { break; }
            searchAns.push(result2);
        } if (searchAns.indexOf(-1) === 0) { searchAfter(trCount); } else {
            searchResult(searchAns, trCount);
        }
    }) const searchAfter = (trCount) => {

        var count = 0;

        for (var i = 0; i < bookListName.length; i++) {
            var bookimg = bookListimage[i]; var bookName = bookListName[i]; if (i == 0 ||
                i % trCount == 0) { $('<tr class="book_stage" id="table_' + i + '_stage">
        </tr > ').appendTo('.imageTable');

    count = i;

}

        $('<td id="book_' + i + '_stage"></td>').appendTo('#table_' + count + '_stage');
$('<div id="content_' + i + '_id" class="contents-item"></div>').appendTo('#book_' + i + '_stage');
// $('<button type="submit" name="bookNum" id="kind"
class="popup_"+i+"_button" ></button > ").appendTo('#content_'+i+'_id');
$('<label for="Osaka" class="book' + i + 'Image"></label>').insertAfter('#content_' + i + '_id');
$('<a id="a' + i + 'Tab" href="#"></a>').appendTo('#content_' + i + '_id');
$('<img src=' + bookimg + ' id=book' + i + 'Image>').appendTo('#a' + i + 'Tab');
$('<p id="book' + i + 'Name">' + bookName + '</p>').insertAfter('.book' + i + 'Image');

        }
        };

const searchResult = (searchAns, trCount) => {

    var count = 0;

    for (var i = 0; i < searchAns.length; i++) {
        var bookimg = bookListimage[searchAns[i]]; var
            bookName = bookListName[searchAns[i]]; if (i == 0 || i % trCount == 0) {
                $('<tr class="book_stage"
            id = "table_'+i+'_stage" >
            </tr > ').appendTo('.imageTable');

count = i;

            }
$('<td id="book_' + i + '_stage"></td>').appendTo('#table_' + count + '_stage');
$('<div id="content_' + i + '_id" class="contents-item"></div>').appendTo('#book_' + i + '_stage');
// $('<button type="submit" name="bookNum" id="kind"
class="popup_'+i+'_button" ></button > ').appendTo('#content_'+i+'_id');
$('<label for="Osaka" class="book' + i + 'Image"></label>').insertAfter('#content_' + i + '_id');
$('<a id="a' + i + 'Tab" href="#"></a>').appendTo('#content_' + i + '_id');
$('<img src=' + bookimg + ' id=book' + i + 'Image>').appendTo('#a' + i + 'Tab');
$('<p id="book' + i + 'Name">' + bookName + '</p>').insertAfter('.book' + i + 'Image');

            }


            }





            })