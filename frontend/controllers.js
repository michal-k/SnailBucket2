var snailBucketApp = angular.module('snailBucketApp', []);

snailBucketApp.controller('TournamentsCtrl', function ($scope) {
  $scope.tournaments = [
    { 'name': 'Snail Bucket 4',
      'rounds': ['1', '2', '3'] },
    { 'name': 'Snail Bucket Monthly 2015',
      'rounds': ['1'] }
  ];
});

snailBucketApp.controller('NewsCtrl', function ($scope, $sce) {
  $scope.newsitems = [
    { 'date': 'Wed, 9th Sep 2015',
      'text': $sce.trustAsHtml('We have generated Round 2 pairings. We would like to thank you for your patience, and ask you to report any problems to us. The initial deadline will be 12th September.') },
    { 'date': 'Sat, 5th Sep 2015',
      'text': $sce.trustAsHtml('We have a major software problem and cannot currently create new pairings for the Monthly. The start of round 2 will be delayed by one week. We\'d like to apologize to all participants.')},
    { 'date': 'Mon, 3rd Aug 2015',
      'text': $sce.trustAsHtml('Round 1 pairings for the SB Monthly 2015 have been posted. We ask that you take a look at the <a href="/wiki/SBMonthlyTourneyGuide#Scheduling" title="SBMonthlyTourneyGuide">scheduling deadlines</a>, if you have not yet done so; they differ from both Teamleague and our regular SB tourneys. Sadly, a persistent bug keeps Game forum posts from being emailed to you. Please access your Game forum regularly, until we solve this annoying problem. <b>Update</b>: An encouraging number of users reports that email forwarding is now working.') },
    { 'date': 'Tue, 28 Jul 2015',
      'text': '<b>New members</b>: We have some problems with sending activation emails. If you join us, and don&#39;t get your activation email in 10 minutes, please email tds@snailbucket.org.' },
    { 'date': 'Wed, 15 Jul 2015',
      'text': 'We invite you to and look forward to the <font color="green"><b>SB Monthly 2015</b></font> very much, a 5-round tournament with one game per month! You may sign up until Jul 29th at 0300 GMT; the tournament is scheduled to begin on Aug 3rd. If you have created an account on our website already and your name <a class="externallink" href="http://snailbucket.org/members" rel="nofollow" title="http://snailbucket.org/members">is in this list</a>, simply log in and <a class="externallink" href="http://snailbucket.org/tourney/signup/monthly15" rel="nofollow" title="http://snailbucket.org/tourney/signup/monthly15">sign up</a> to the tourney. If you have not yet created an account, please do so first, following the instructions in the <a href="/wiki/SBMonthlyTourneyGuide" title="SBMonthlyTourneyGuide">Tourney Guide</a>.' }
  ];
});

snailBucketApp.controller('ViewCtrl', function ($scope) {
  $scope.currentView = 'main';
  $scope.changeView = function(newView) {
    $( "li" ).removeClass('active');
    $scope.currentView = newView;
    $( '#' + newView ).addClass('active');
  };
  $scope.getCurrent = function() {
    return $scope.currentView + '.html';
  };
});
