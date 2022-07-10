/*********************************************
 * OPL 22.1.0.0 Model
 * Author: gstew
 * Creation Date: Jul 7, 2022 at 3:05:37 PM
 *********************************************/

 tuple Pair {
   string a;
   string b;
 }
 
 tuple Requirement {
   string courseCode;
   int requireSlots;
 }
 
 {Pair} TeacherCourseAssignment = ...;
 {Requirement} RequirementSet = ...;
 {string} DaysInWeek = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"};
 int SlotsPerDay = ...;
 int MaxTime = SlotsPerDay;
 range Time = 0..MaxTime-1;
 int MaxSlotsInARow = 3; 
 
 dvar int Start[RequirementSet] in Time;
 dvar int End[RequirementSet] in Time;
 dvar int Days[RequirementSet][DaysInWeek] in 0..1; 
 dvar int DaysOccured in 1..3;
 dvar int MaxOccurencesPerDay in 0..card(RequirementSet)*3;
 
 minimize MaxOccurencesPerDay;
 
 subject to {
   forall(r in RequirementSet) {
      End[r] >= Start[r] + 1;
      End[r] - Start[r] <= MaxSlotsInARow;
   }
   
   forall(r in RequirementSet) {
     sum(d in DaysInWeek) Days[r][d] <= 3;
     sum(d in DaysInWeek) Days[r][d] * (End[r] - Start[r]) == r.requireSlots;
   }
   
 }