# Documentation File
You will find here all the descriptions of the core concepts and ideas of this app.

## Introduction
Someday we had this idea about an **online space** where we could **stayed tuned** with friends, **listening to the same music at the same time**, and messaging about it in real time. A space where we could all **push music**, and make it play on a **24/7 web radio** where **only the people you want** could join and enjoy. A or some web radios. Depending on the style, the years, or the will of your users. **Making us able to pop, manage and kill private web radio streams in a second**.

## Definitions
### Main Concepts
The following are hierarchy levels of rights and application layers. Every entity with the same level are associated between each other. In this logic, level (1) monitors all level (2) entities, as level (2) monitors all level (3) entities.
#### Application Levels (Level)
* (1) - **_App Instance_** : The _App Instance_ denotes the entire application at a hosting system level. It groups all the conceptual elements of the app entity, like _Teams_, _Pools_, _Users_, _Channels_, etc... The _App Instance_ is associated to a global _Admin_ (see _Users Level_ section bellow).

* (2) - **_Team_** : A _Team_ denotes a group of authenticable users and is administrated by one of them, the _Team Chief_ (see _User Levels_ section bellow). Every team have a unique name on the _App Instance_ and is associated to a _Pool_. They also have a limited number of _Channels_ defined by the global _Admin_.

* (2) - **_Pool_** : A _Pool_ denotes all music files available for it associated _Team_. It is administrated by the _Team Chief_ and every user can add music to it by uploading their own files, filling the meta-datas and, in some cases, bind them to _Channels_. In a word, a _Pool_ is a big table which makes the link between physical files and his related _Team_ track and meta-data database.

* (3) - **_Channel_** : A _Channel_ denotes a virtual room administrated by the _Chief_ that authenticated users can join for listening to music and chat about it. Every channel is associated to a _Stream_, provided by the application back-office (icecast). Some parts of the _Pool_ can be associated directly to a _Channel_,

* (3) - **_Stream_** : a _Stream_ denotes a icecast server mount point which requires authentication to allow a user to listen to the _Stream_, preventing unwanted users on your bandwidth.

#### Role Levels (Level)
* (1) - **_Admin_** : The _Admin_ of the app have every possible rights. He can monitor each logic elements of the app (storage, networking, app configuration, etc...). He regulates physical resources of the hosting machine by restricting for example Disc Usage and CPU for each _Team_. The _Admin_ has the possibility to invite somebody by mail in order to create a new _Team_, and consequently a new _Pool_ entity and a _User_ account promoted after _Admin_ validation as a _Chief_.

* (2) - **_Chief_** : The _Chief_ denotes the "_Team_ admin". He has all rights in it, except for the restrictions set by the _Admin_ (f.e. number of _Channels_, of _Users_, storage limit, bandwidth, etc...). The _Chief_ can invite and accept request for creating new _Users_ and manage them, create new _Channel_, manage the _Pool_, edit meta-datas, remove tracks, and manage _Stream_ behaviours.

* (3) - **_User_** : The _User_ denotes the regular application user. The _User_ can be related to only one _Team_ (_User_ accounts aren't cross-_Team_). When unauthenticated, the _User_ can't do anything except log in or ask for the creation of a new account in a _Team_ to his related _Chief_. Once logged, the _User_ can join every _Channel_ of the _Team_, post messages in it and, the most important, get access to the _Stream_ attached to each _Channel_. Finally, he can also upload new audio files on the server adding them to the _Pool_, and optionally attach them to one or many _Channels_.

## Features
This represents a non-exhaustive list of possible features we would like to integrate to this application.

* Guest accounts (priority) -> Permit an unauthenticated user to join a _Channel_ temporarily
* Private messaging is kind of a "must-have" feature.
* Administrator contact by escalated messages (from _User_ to _Chief_, then from _Chief_ to _Admin_).
* Possibility to custom _Stream_ behaviour by an upvote and downvote system, and a report system for corrupted songs or just unbelievable [shitty music](https://duckduckgo.com/?q=shitty+fluted&t=lm&ia=videos&iax=1&iai=V0Tv1Y4RvVo "totally safe link for your ears. Trust me.") =|
* Past songs tracklist as a scopable timeline, retrieving every messages of the chat sent for each son played in a _Channel_.

## Flow Diagrams

(More incomming ...)
* [File Upload](https://github.com/Clement-Ruiz/radio-bretzel/tree/papyDocker/documentation/flow_diagrams/Flow-Diagram-File-Upload.pdf)
* [Team Creation](https://github.com/Clement-Ruiz/radio-bretzel/blob/dockerizing/documentation/flow_diagrams/Flow-Diagram-Team-Creation.pdf)
* [User Creation](https://github.com/Clement-Ruiz/radio-bretzel/blob/dockerizing/documentation/flow_diagrams/Flow-Diagram-User-Creation.pdf)
* [Stream Creation](https://github.com/Clement-Ruiz/radio-bretzel/blob/dockerizing/documentation/flow_diagrams/Flow-Diagram-Stream-Creation.pdf)
